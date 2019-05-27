#pragma once

#include <todo/todo.pb.h>
#include <todo/todo.grpc.pb.h>
#include <grpcpp/grpcpp.h>
#include <memory>
#include <string>

namespace gateway
{

class ToDoClient final
{
public:
  explicit ToDoClient(std::unique_ptr<ToDo::Stub> pStub)
    : m_pStub(std::move(pStub))
  {
  }
  ~ToDoClient() = default;
  ToDoClient(const ToDoClient&) = delete;
  ToDoClient(ToDoClient&&) = delete;
  ToDoClient& operator=(const ToDoClient&) = delete;
  ToDoClient& operator=(ToDoClient&&) = delete;

  grpc::Status createToDo(
    const std::string& rUserToken,
    const CreateToDoReq& rRequest,
    CreateToDoRsp& rResponse)
  {
    auto pContext = ToDoClientContextBuilder().setUserToken(rUserToken).build();
    return m_pStub->CreateToDo(pContext.get(), rRequest, &rResponse);
  }
  grpc::Status getToDo(
    const std::string& rUserToken,
    const GetToDoReq& rRequest,
    GetToDoRsp& rResponse)
  {
    auto pContext = ToDoClientContextBuilder().setUserToken(rUserToken).build();
    return m_pStub->GetToDo(pContext.get(), rRequest, &rResponse);
  }
  grpc::Status deleteToDo(
    const std::string& rUserToken,
    const DeleteToDoReq& rRequest,
    DeleteToDoRsp& rResponse)
  {
    auto pContext = ToDoClientContextBuilder().setUserToken(rUserToken).build();
    return m_pStub->DeleteToDo(pContext.get(), rRequest, &rResponse);
  }
  grpc::Status updateToDo(
    const std::string& rUserToken,
    const UpdateToDoReq& rRequest,
    UpdateToDoRsp& rResponse)
  {
    auto pContext = ToDoClientContextBuilder().setUserToken(rUserToken).build();
    return m_pStub->UpdateToDo(pContext.get(), rRequest, &rResponse);
  }
  grpc::Status listToDo(
    const std::string& rUserToken,
    const ListToDoReq& rRequest,
    ListToDoRsp& rResponse)
  {
    auto pContext = ToDoClientContextBuilder().setUserToken(rUserToken).build();
    return m_pStub->ListToDo(pContext.get(), rRequest, &rResponse);
  }

private:
  class ToDoClientContextBuilder
  {
  using Self = ToDoClientContextBuilder;
  using Ctxt = grpc::ClientContext;
  using CtxtPtr = std::unique_ptr<Ctxt>;
  public:
    ToDoClientContextBuilder() = default;
    ~ToDoClientContextBuilder() = default;

    Self& setUserToken(const std::string& rUserToken)
    {
      m_pContext->AddMetadata(m_kUserTokenKey, rUserToken);
      return *this;
    }

    CtxtPtr build()
    {
      return std::move(m_pContext);
    }

  private:
    CtxtPtr m_pContext = std::make_unique<Ctxt>();
    const std::string m_kUserTokenKey{"user-token"};
  };

  std::unique_ptr<ToDo::Stub> m_pStub;
};

}
