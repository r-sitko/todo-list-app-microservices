#pragma once

#include <gateway/userclient.hpp>
#include <user/user.pb.h>
#include <user/user.grpc.pb.h>
#include <grpcpp/grpcpp.h>

namespace gateway
{

class UserServiceImpl final : public User::Service
{
public:
  explicit UserServiceImpl(std::unique_ptr<UserClient> pClient)
    : m_pClient(std::move(pClient))
  {
  }
  ~UserServiceImpl() = default;
  UserServiceImpl(const UserServiceImpl&) = delete;
  UserServiceImpl(UserServiceImpl&&) = delete;
  UserServiceImpl& operator=(const UserServiceImpl&) = delete;
  UserServiceImpl& operator=(UserServiceImpl&&) = delete;

private:
  grpc::Status Login(
    grpc::ServerContext* pContext,
    const LoginReq* pRequest,
    LoginRsp* pReply) final
  {
    (void)pContext;
    return m_pClient->login(*pRequest, *pReply);
  }
  grpc::Status Register(
    grpc::ServerContext* pContext,
    const RegisterReq* pRequest,
    RegisterRsp* pReply) final
  {
    (void)pContext;
    return m_pClient->registerCall(*pRequest, *pReply);
  }

  std::unique_ptr<UserClient> m_pClient;
};

}
