from alembic import op
from sqlalchemy.sql import text
from typing import Sequence, Union

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
    test_data = [
        {'user_id': 1, 'date': '2024-01-21', 'amount': 3000.0, 'time': 100, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-22', 'amount': 4000.0, 'time': 220, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-23', 'amount': 5000.0, 'time': 120, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-24', 'amount': 6000.0, 'time': 220, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-25', 'amount': 7000.0, 'time': 203, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-26', 'amount': 1000.0, 'time': 202, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-27', 'amount': 3200.0, 'time': 120, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-28', 'amount': 3300.0, 'time': 200, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-29', 'amount': 3400.0, 'time': 200, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-30', 'amount': 3500.0, 'time': 230, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-01-31', 'amount': 3600.0, 'time': 500, 'tax': 11000.0},
        {'user_id': 1, 'date': '2024-02-01', 'amount': 3700.0, 'time': 200, 'tax': 11000.0},
    ]

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
