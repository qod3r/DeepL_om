from app.dao.base import BaseDAO
from app.study.models import Studies


class StudiesDAO(BaseDAO):
    model = Studies