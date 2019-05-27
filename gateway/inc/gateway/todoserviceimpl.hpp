#pragma once

#include <gateway/todoclient.hpp>
#include <todo/todo.pb.h>
#include <todo/todo.grpc.pb.h>
#include <grpcpp/grpcpp.h>
#include <vector>

namespace gateway
{

class ToDoServiceImpl final : public ToDo::Service
{
public:
  explicit ToDoServiceImpl(std::unique_ptr<ToDoClient> pClient)
    : m_pClient(std::move(pClient))
  {
  }
  ~ToDoServiceImpl() = default;
  ToDoServiceImpl(const ToDoServiceImpl&) = delete;
  ToDoServiceImpl(ToDoServiceImpl&&) = delete;
  ToDoServiceImpl& operator=(const ToDoServiceImpl&) = delete;
  ToDoServiceImpl& operator=(ToDoServiceImpl&&) = delete;

private:
  grpc::Status CreateToDo(
    grpc::ServerContext* pContext,
    const CreateToDoReq* pRequest,
    CreateToDoRsp* pReply) final
  {
    return m_pClient->createToDo(getUserTokenFromAuthContext(*pContext), *pRequest, *pReply);
  }
  grpc::Status GetToDo(
    grpc::ServerContext* pContext,
    const GetToDoReq* pRequest,
    GetToDoRsp* pReply) final
  {
    return m_pClient->getToDo(
      getUserTokenFromAuthContext(*pContext), *pRequest, *pReply);
  }
  grpc::Status DeleteToDo(
    grpc::ServerContext* pContext,
    const DeleteToDoReq* pRequest,
    DeleteToDoRsp* pReply) final
  {
    return m_pClient->deleteToDo(
      getUserTokenFromAuthContext(*pContext), *pRequest, *pReply);
  }
  grpc::Status UpdateToDo(
    grpc::ServerContext* pContext,
    const UpdateToDoReq* pRequest,
    UpdateToDoRsp* pReply) final
  {
    return m_pClient->updateToDo(
      getUserTokenFromAuthContext(*pContext), *pRequest, *pReply);
  }
  grpc::Status ListToDo(
    grpc::ServerContext* pContext,
    const ListToDoReq* pRequest,
    ListToDoRsp* pReply) final
  {
    return m_pClient->listToDo(
      getUserTokenFromAuthContext(*pContext), *pRequest, *pReply);
  }

  std::string getUserTokenFromAuthContext(const grpc::ServerContext& rContext) const
  {
    std::vector<grpc::string_ref> tokenVec =
      rContext.auth_context()->FindPropertyValues("user-token");
    return std::string(tokenVec.at(0).cbegin(), tokenVec.at(0).cend());
  }

  std::unique_ptr<ToDoClient> m_pClient;
};

}
