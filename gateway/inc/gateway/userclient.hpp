#pragma once

#include <user/user.pb.h>
#include <user/user.grpc.pb.h>
#include <grpcpp/grpcpp.h>
#include <memory>

namespace gateway
{

class UserClient final
{
public:
  explicit UserClient(std::unique_ptr<User::Stub> pStub)
    : m_pStub(std::move(pStub))
  {
  }
  ~UserClient() = default;
  UserClient(const UserClient&) = delete;
  UserClient(UserClient&&) = delete;
  UserClient& operator=(const UserClient&) = delete;
  UserClient& operator=(UserClient&&) = delete;

  grpc::Status login(const LoginReq& rRequest, LoginRsp& rResponse)
  {
    grpc::ClientContext context;
    return m_pStub->Login(&context, rRequest, &rResponse);
  }

  grpc::Status registerCall(const RegisterReq& rRequest, RegisterRsp& rResponse)
  {
    grpc::ClientContext context;
    return m_pStub->Register(&context, rRequest, &rResponse);
  }

private:
  std::unique_ptr<User::Stub> m_pStub;
};

}
