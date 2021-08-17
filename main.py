from re import A
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.operators import exists

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
    		return f"Video(user_id = {user_id}, password = {password})"

# db.create_all();

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("user_id", type = str, help = "user_id needed", required = True)
account_put_args.add_argument("password", type = str, help = "password needed", required = True)

account_update_args = reqparse.RequestParser()
account_update_args.add_argument("user_id", type = str, help = "user_id needed")
account_update_args.add_argument("password", type = str, help = "password needed")


resource_fields = {
    'id' : fields.Integer,
    'user_id' : fields.String,
    'password' : fields.String
}


class Account(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = AccountModel.query.filter_by(id = id).first()
        if not result:
            abort(404, message = "cannot find account")
        return result

    @marshal_with(resource_fields)
    def put(self, id):
        args = account_put_args.parse_args()
        result = AccountModel.query.filter_by(id = id).first()
        if result :
            abort(409, message = "account id taken")

        account = AccountModel(id = id, user_id = args['user_id'], password = args['password'])
        db.session.add(account)
        db.session.commit()
        return account

    @marshal_with(resource_fields)
    def patch(self, id):
        args = account_update_args.parse_args()
        result = AccountModel.query.filter_by(id = id).first()
        if not result:
            abort(404, message = "account doesn't exist, cannot update")
        
        if args['user_id'] :
            result.user_id = args['user_id']

        if args['password']:
            result.password = args['password']

        db.session.commit()

        return result
    
    def delete(self, id):
        result = AccountModel.query.filter_by(id = id).first()
        if not result:
            abort(404, message = "cannot find account")
        AccountModel.query.filter_by(id = id).delete()
        db.session.commit()
        


api.add_resource(Account, "/mygame/<int:id>")


if __name__ == "__main__":
    app.run(debug=True)