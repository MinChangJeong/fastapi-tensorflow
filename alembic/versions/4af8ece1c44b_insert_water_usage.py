from alembic import op
from sqlalchemy.sql import text
from typing import Sequence, Union
import random
from datetime import datetime, timedelta

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4af8ece1c44b'
down_revision: Union[str, None] = '6e820e3cb17c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 데이터베이스 연결을 가져옵니다.
    connection = op.get_bind()

    # 테스트 데이터를 생성하고 삽입합니다.
    start_date = datetime(2023, 12, 1)
    end_date = datetime(2024, 1, 31)

    test_data = []

    for _ in range((end_date - start_date).days + 1):
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        random_amount = round(random.uniform(1000, 30000), 2)
        random_time = random.randint(10, 250)
        random_tax = round(random.uniform(30, 3000), 2)

        data = {
            'user_id': 1,
            'date': random_date.strftime('%Y-%m-%d'),
            'amount': random_amount,
            'time': random_time,
            'tax': random_tax,
        }

        test_data.append(data)

    for data in test_data:
        connection.execute(
            text(
                """
                INSERT INTO water_usage (user_id, date, amount, time, tax)
                VALUES (:user_id, :date, :amount, :time, :tax)
                """
            ).bindparams(
                user_id=data['user_id'],
                date=data['date'],
                amount=data['amount'],
                time=data['time'],
                tax=data['tax'],
            )
        )

def downgrade():
    # 역으로 마이그레이션을 되돌리는 코드를 작성합니다.
    op.drop_table('water_usage')
