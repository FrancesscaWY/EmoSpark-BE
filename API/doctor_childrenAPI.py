from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotion_system.db'  # 指向你的数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 使用现有表结构（无需重新定义）
class ChildTherapist(db.Model):
    __tablename__ = 'ChildTherapists'  # 注意表名大小写需与实际一致
    __table_args__ = {'extend_existing': True}  # 如果模型类已定义过则扩展

    # 以下字段会自动映射到现有表
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('Children.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    assigned_at = db.Column(db.DateTime)


@app.route('/doctor/<int:child_id>/<int:therapist_id>', methods=['POST'])
def associate_child_therapist(child_id, therapist_id):
    # 验证基础参数
    if not child_id or not therapist_id:
        raise BadRequest("child_id and therapist_id are required")

    # 验证儿童和心理师是否存在（通过外键关联表）
    child_exists = db.session.execute(
        db.select(db.exists().where(db.text('Children.id = :child_id'))),
        {'child_id': child_id}
    ).scalar()

    therapist_exists = db.session.execute(
        db.select(db.exists().where(db.text('Users.id = :therapist_id AND user_type = "therapist"'))),
        {'therapist_id': therapist_id}
    ).scalar()

    if not child_exists or not therapist_exists:
        raise NotFound("Child or therapist not found")

    try:
        # 处理分配时间
        assigned_at = datetime.utcnow()
        if request.json and 'assigned_at' in request.json:
            assigned_at = datetime.fromisoformat(request.json['assigned_at'])

        # 创建关联记录
        association = ChildTherapist(
            child_id=child_id,
            therapist_id=therapist_id,
            assigned_at=assigned_at
        )

        db.session.add(association)
        db.session.commit()

        return jsonify({
            "child_id": child_id,
            "therapist_id": therapist_id,
            "assigned_at": assigned_at.isoformat()
        }), 201

    except ValueError as e:
        raise BadRequest(f"Invalid datetime format: {str(e)}")
    except Exception as e:
        db.session.rollback()
        raise BadRequest(f"Database error: {str(e)}")


# 错误处理器保持不变...

# 错误处理器
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 400


@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True)