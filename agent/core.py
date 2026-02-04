"""
Agent Core - Main Orchestrator

Coordinates between:
- LLM (Ollama) for reasoning
- Tool registry for execution
- Memory for context
- Safety layer for validation
"""

from typing import List, Dict, Any, Optional, AsyncIterator
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio
from datetime import datetime

import structlog
from pydantic import BaseModel

from tools.base import ToolRegistry, ToolResult, RiskLevel
from security.command_filter import CommandFilter, SafetyLevel

logger = structlog.get_logger()


class AgentState(Enum):
    """Agent execution states."""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING_APPROVAL = "waiting_approval"
    RESPONDING = "responding"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Message in the agent conversation."""
    role: str  # system, user, assistant, tool
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """Plan for executing a task."""
    goal: str
    steps: List[Dict[str, Any]]
    risk_assessment: str
    estimated_steps: int


class AgentConfig(BaseModel):
    """Configuration for the agent."""
    model: str = "qwen2.5:7b"
    temperature: float = 0.5
    max_tokens: int = 4096
    context_window: int = 128000
    auto_execute_safe: bool = True
    require_approval_for: List[str] = ["approval", "blocked"]


class DevOpsAgent:
    """
    Main DevOps AI Agent.
    
    Responsibilities:
    1. Parse user intent
    2. Plan task execution
    3. Coordinate with LLM
    4. Execute tools safely
    5. Maintain conversation context
    """
    
    def __init__(
        self,
        llm_client: Any,  # OllamaClient
        tool_registry: ToolRegistry,
        command_filter: CommandFilter,
        config: Optional[AgentConfig] = None
    ):
        self.llm = llm_client
        self.tools = tool_registry
        self.safety = command_filter
        self.config = config or AgentConfig()
        
        self.state: AgentState = AgentState.IDLE
        self.conversation: List[AgentMessage] = []
        self.pending_approvals: List[Dict] = []
        
        self.logger = structlog.get_logger(agent="DevOpsAgent")
    
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """
        Main chat interface with streaming response.
        
        Args:
            user_input: User's natural language request
            
        Yields:
            Response chunks as they are generated
        """
        self.logger.info("chat_started", user_input=user_input)
        
        # Add user message to context
        self.conversation.append(AgentMessage(role="user", content=user_input))
        
        # Step 1: Understand intent and plan
        self.state = AgentState.THINKING
        plan = await self._create_plan(user_input)
        
        if plan.estimated_steps == 0:
            # Simple question, no tools needed
            async for chunk in self._generate_response(user_input):
                yield chunk
            return
        
        # Step 2: Execute plan
        self.state = AgentState.EXECUTING
        results = []
        
        for step in plan.steps:
            result = await self._execute_step(step)
            results.append(result)
            
            if not result.success:
                yield f"❌ Step failed: {result.error}\\n"
                break
        
        # Step 3: Generate final response
        self.state = AgentState.RESPONDING
        async for chunk in self._synthesize_response(plan, results):
            yield chunk
        
        self.state = AgentState.IDLE
    
    async def _create_plan(self, user_input: str) -> ExecutionPlan:
        """
        Create an execution plan for the user's request.
        
        Args:
            user_input: User's request
            
        Returns:
            ExecutionPlan with steps
        """
        # Build planning prompt
        available_tools = self.tools.list_all()
        
        planning_prompt = f"""
You are a DevOps AI Agent. Analyze the user's request and create a plan.

User Request: {user_input}

Available Tools:
{json.dumps(available_tools, indent=2)}

Respond in JSON format:
{{
    "goal": "Clear statement of what the user wants",
    "needs_tools": true/false,
    "steps": [
        {{
            "tool": "tool_name",
            "operation": "operation_name",
            "parameters": {{}},
            "reason": "Why this step is needed"
        }}
    ],
    "risk_assessment": "safe|read_only|requires_approval",
    "clarifying_questions": ["question1", "question2"]  // if ambiguous
}}

Rules:
- Use tools only when necessary
- Prefer read-only operations
- Flag any destructive operations
- Ask questions if the request is ambiguous
"""
        
        # Get plan from LLM
        response = await self.llm.generate(
            model=self.config.model,
            prompt=planning_prompt,
            format="json",
            temperature=0.3
        )
        
        try:
            plan_data = json.loads(response)
            
            # Check for clarifying questions
            if plan_data.get("clarifying_questions"):
                questions = "\\n".join(plan_data["clarifying_questions"])
                return ExecutionPlan(
                    goal="Clarification needed",
                    steps=[],
                    risk_assessment="safe",
                    estimated_steps=0
                )
            
            return ExecutionPlan(
                goal=plan_data.get("goal", user_input),
                steps=plan_data.get("steps", []),
                risk_assessment=plan_data.get("risk_assessment", "safe"),
                estimated_steps=len(plan_data.get("steps", []))
            )
        except json.JSONDecodeError:
            self.logger.error("plan_parse_failed", response=response)
            return ExecutionPlan(
                goal=user_input,
                steps=[],
                risk_assessment="safe",
                estimated_steps=0
            )
    
    async def _execute_step(self, step: Dict[str, Any]) -> ToolResult:
        """
        Execute a single step from the plan.
        
        Args:
            step: Step definition with tool, operation, parameters
            
        Returns:
            ToolResult from execution
        """
        tool_name = step.get("tool")
        operation = step.get("operation")
        parameters = step.get("parameters", {})
        
        # Get tool
        tool = self.tools.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found"
            )
        
        # Check safety
        risk_level = tool.get_risk_level(operation, **parameters)
        
        if risk_level == RiskLevel.BLOCKED:
            return ToolResult(
                success=False,
                error=f"Operation '{operation}' is blocked for safety",
                risk_level=risk_level
            )
        
        if risk_level == RiskLevel.REQUIRES_APPROVAL:
            if not self.config.auto_execute_safe:
                return ToolResult(
                    success=False,
                    error=f"Operation '{operation}' requires approval",
                    risk_level=risk_level
                )
        
        # Execute
        try:
            input_data = tool.input_schema(operation=operation, **parameters)
            result = await tool.execute(input_data)
            return result
        except Exception as e:
            self.logger.error("step_execution_failed", 
                            tool=tool_name, operation=operation, error=str(e))
            return ToolResult(
                success=False,
                error=str(e),
                risk_level=risk_level
            )
    
    async def _generate_response(self, user_input: str) -> AsyncIterator[str]:
        """
        Generate a direct response without tool use.
        
        Args:
            user_input: User's question
            
        Yields:
            Response chunks
        """
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        async for chunk in self.llm.chat_stream(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature
        ):
            yield chunk
    
    async def _synthesize_response(
        self, 
        plan: ExecutionPlan, 
        results: List[ToolResult]
    ) -> AsyncIterator[str]:
        """
        Synthesize final response from plan and results.
        
        Args:
            plan: Original execution plan
            results: Results from each step
            
        Yields:
            Response chunks
        """
        # Build synthesis prompt
        synthesis_prompt = f"""
You are a DevOps AI Agent. Summarize the results for the user.

Goal: {plan.goal}

Execution Results:
"""
        for i, result in enumerate(results, 1):
            synthesis_prompt += f"\\nStep {i}:\\n"
            synthesis_prompt += f"  Success: {result.success}\\n"
            synthesis_prompt += f"  Data: {result.data}\\n"
            if result.warnings:
                synthesis_prompt += f"  Warnings: {result.warnings}\\n"
        
        synthesis_prompt += """

Provide a clear summary:
1. What was done
2. Key findings
3. Any issues or warnings
4. Recommended next steps
"""
        
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": synthesis_prompt}
        ]
        
        async for chunk in self.llm.chat_stream(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature
        ):
            yield chunk
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the LLM."""
        return """You are a DevOps AI Agent that helps engineers with daily tasks.

Core Principles:
1. Safety First: Never execute destructive commands without approval
2. Transparency: Explain what you're doing and why
3. Accuracy: Verify information before presenting it
4. Helpfulness: Provide actionable recommendations

When suggesting commands:
- Use explicit flags (no aliases)
- Include comments explaining non-obvious options
- Show the expected output
- Explain any risks

You have access to tools for Docker, Kubernetes, Helm, Terraform, Ansible, Git, and shell commands.
Always prefer read-only operations when possible.
"""
    
    def get_state(self) -> AgentState:
        """Get current agent state."""
        return self.state
    
    def get_conversation_history(self) -> List[AgentMessage]:
        """Get conversation history."""
        return self.conversation.copy()
    
    def clear_context(self) -> None:
        """Clear conversation context."""
        self.conversation.clear()
        self.logger.info("context_cleared")
