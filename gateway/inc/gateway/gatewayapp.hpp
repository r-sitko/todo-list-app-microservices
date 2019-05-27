#pragma once

#include <gateway/config.hpp>
#include <gateway/gatewayauthmetadataprocessor.hpp>
#include <gateway/userserviceimpl.hpp>
#include <gateway/todoserviceimpl.hpp>
#include <grpcpp/grpcpp.h>
#include <memory>

namespace gateway
{

class GatewayApp final
{
public:
  explicit GatewayApp(std::shared_ptr<gateway::Config> pConfig);
  ~GatewayApp() = default;
  GatewayApp(const GatewayApp&) = delete;
  GatewayApp(GatewayApp&&) = delete;
  GatewayApp& operator=(const GatewayApp&) = delete;
  GatewayApp& operator=(GatewayApp&&) = delete;

  void init();
  void run();
  void deInit();

private:
  std::shared_ptr<gateway::Config> m_pConfig;
  std::shared_ptr<GatewayAuthMetadataProcessor> m_pAuthProcessor;
  std::unique_ptr<gateway::UserServiceImpl> m_pUserService;
  std::unique_ptr<gateway::ToDoServiceImpl> m_pToDoService;
  std::unique_ptr<grpc::Server> m_pServer;
};

}
