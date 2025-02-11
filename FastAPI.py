import jwt
import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# 创建FastAPI应用程序实例
app = FastAPI()


# 定义一个根路径（/）的路由，访问此路径时返回一个欢迎消息
@app.get("/")
def home():
    return {"message": "Welcome to the API"}


# 定义一个用于签名和验证JWT的密钥
SECRET_KEY = "secret"
# 定义OAuth2密码流，tokenUrl是令牌端点
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 创建一个JWT令牌，数据字典包含要编码到令牌中的数据
def create_token(data: dict):
    # 设置令牌过期时间为当前时间加1小时
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    # 使用密钥和HS256算法对数据进行编码，生成JWT令牌
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


# 定义一个生成令牌的路由，访问此路径时返回生成的令牌
@app.post("/token")
def generate_token():
    # 调用create_token函数生成令牌，并返回令牌和令牌类型
    return {"access_token": create_token({"user": "test_user"}), "token_type": "bearer"}


# 定义一个受保护的路由，访问此路径时需要提供JWT令牌进行验证
@app.get("/secure-data")
def secure_data(token: str = Depends(oauth2_scheme)):
    try:
        # 解码JWT令牌，验证令牌的有效性
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # 返回包含用户信息的消息
        return {"message": f"Hello, {payload['user']}!"}
    except jwt.ExpiredSignatureError:
        # 令牌过期时抛出401错误
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        # 令牌无效时抛出401错误
        raise HTTPException(status_code=401, detail="Invalid token")


# 启动Uvicorn服务器，运行FastAPI应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
