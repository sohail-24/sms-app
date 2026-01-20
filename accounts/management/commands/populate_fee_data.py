from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Student, Fee, Payment
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate sample fee data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample fee data...')
        
        # Get all students
        students = Student.objects.all()
        
        if not students.exists():
            self.stdout.write(self.style.ERROR('No students found. Please create students first.'))
            return
        
        # Clear existing fees and payments for clean test
        Fee.objects.all().delete()
        Payment.objects.all().delete()
        
        fee_types = [
            ('Tuition Fee', 1500.00),
            ('Laboratory Fee', 200.00),
            ('Library Fee', 100.00),
            ('Sports Fee', 150.00),
            ('Examination Fee', 300.00),
        ]
        
        payment_methods = ['CREDIT_CARD', 'DEBIT_CARD', 'NET_BANKING', 'UPI', 'CASH']
        payment_statuses = ['completed', 'pending', 'failed']
        
        for student in students:
            self.stdout.write(f'Creating fees for {student.get_full_name()}...')
            
            # Create 3-5 fee records per student
            num_fees = random.randint(3, 5)
            total_student_fees = 0
            
            for i in range(num_fees):
                fee_type, base_amount = random.choice(fee_types)
                amount = base_amount + random.uniform(-50, 100)  # Add some variation
                
                # Create fees with different due dates
                due_date = timezone.now().date() + timedelta(days=random.randint(-30, 90))
                
                fee = Fee.objects.create(
                    student=student,
                    amount=amount,
                    due_date=due_date,
                    paid=random.choice([True, False]) if i < num_fees - 1 else False,  # Keep last one unpaid
                    description=fee_type,
                    payment_date=due_date - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None
                )
                
                total_student_fees += amount
                
                # Create some payments for paid fees
                if fee.paid:
                    payment = Payment.objects.create(
                        student=student,
                        amount=fee.amount,
                        payment_date=fee.payment_date or timezone.now(),
                        payment_method=random.choice(payment_methods),
                        status='completed',
                        transaction_id=f'TXN{random.randint(100000, 999999)}',
                        remarks=f'Payment for {fee.description}'
                    )
            
            # Create some additional payments (partial payments, overpayments, etc.)
            num_additional_payments = random.randint(0, 2)
            for _ in range(num_additional_payments):
                payment = Payment.objects.create(
                    student=student,
                    amount=random.uniform(50, 500),
                    payment_date=timezone.now() - timedelta(days=random.randint(1, 60)),
                    payment_method=random.choice(payment_methods),
                    status=random.choice(payment_statuses),
                    transaction_id=f'TXN{random.randint(100000, 999999)}',
                    remarks='Additional payment'
                )
        
        # Print summary
        total_fees = Fee.objects.count()
        total_payments = Payment.objects.count()
        total_students = students.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {total_fees} fee records\n'
                f'- {total_payments} payment records\n'
                f'- For {total_students} students'
            )
        ) 