#include <gateway/gatewayapp.hpp>
#include <gateway/userclient.hpp>
#include <gateway/todoclient.hpp>
#include <grpcpp/grpcpp.h>
#include <chrono>
#include <memory>
#include <sstream>

namespace gateway
{

std::string makeServerAddress(
  const std::string& rServiceName,
  uint32_t servicePort)
{
  std::ostringstream ss;
  ss << servicePort;
  std::string portNumber = ss.str();
  std::string serverAddress(rServiceName + ":" + portNumber);
  return serverAddress;
}

void waitForConnectedChannel(
  std::shared_ptr<grpc::Channel> pChannel,
  uint32_t timeoutSec = 10)
{
  std::chrono::system_clock::time_point deadline =
    std::chrono::system_clock::now() + std::chrono::seconds(timeoutSec);
  pChannel->WaitForConnected(deadline);
}


GatewayApp::GatewayApp(std::shared_ptr<gateway::Config> pConfig)
  : m_pConfig{pConfig}
{
}

void GatewayApp::init()
{
  try
  {
    m_pConfig->readConfiguration();
  }
  catch (gateway::NoEnvironmentVariable& rEx)
  {
    std::cerr << rEx;
    throw;
  }
  catch (gateway::FileOpenProblem& rEx)
  {
    std::cerr << rEx;
    throw;
  }

  grpc::SslServerCredentialsOptions::PemKeyCertPair pkcp;
  pkcp.private_key = m_pConfig->getServerPrivateKey();
  pkcp.cert_chain = m_pConfig->getServerCert();

  grpc::SslServerCredentialsOptions ssl_opts;
  ssl_opts.pem_key_cert_pairs.push_back(pkcp);
  ssl_opts.pem_root_certs = "";

  std::shared_ptr<grpc::ServerCredentials> creds = grpc::SslServerCredentials(ssl_opts);
  m_pAuthProcessor = std::make_shared<GatewayAuthMetadataProcessor>(m_pConfig);
  m_pAuthProcessor->addMethodToWhiteList("/User/Login");
  m_pAuthProcessor->addMethodToWhiteList("/User/Register");
  creds->SetAuthMetadataProcessor(m_pAuthProcessor);

  std::string userServerAddress =
    makeServerAddress(
      m_pConfig->getUserServiceName(),
      m_pConfig->getUserServicePort());
  std::string todoServerAddress =
    makeServerAddress(
      m_pConfig->getToDoServiceName(),
      m_pConfig->getToDoServicePort());

  auto pUserChannel = grpc::CreateChannel(
    userServerAddress,
    grpc::InsecureChannelCredentials());
  waitForConnectedChannel(pUserChannel);
  auto pUserStub = User::NewStub(std::move(pUserChannel));
  auto pUserClient = std::make_unique<UserClient>(std::move(pUserStub));
  m_pUserService = std::make_unique<gateway::UserServiceImpl>(std::move(pUserClient));

  auto pToDoChannel = grpc::CreateChannel(
    todoServerAddress,
    grpc::InsecureChannelCredentials());
  waitForConnectedChannel(pToDoChannel);
  auto pToDoStub = ToDo::NewStub(std::move(pToDoChannel));
  auto pToDoClient = std::make_unique<ToDoClient>(std::move(pToDoStub));
  m_pToDoService = std::make_unique<gateway::ToDoServiceImpl>(std::move(pToDoClient));

  std::string gatewayServerAddress =
    makeServerAddress(
      m_pConfig->getServiceName(),
      m_pConfig->getServicePort());

  grpc::ServerBuilder builder;
  builder.AddListeningPort(gatewayServerAddress, creds);
  builder.RegisterService(m_pUserService.get());
  builder.RegisterService(m_pToDoService.get());
  m_pServer = builder.BuildAndStart();
}

void GatewayApp::run()
{
  m_pServer->Wait();
}

void GatewayApp::deInit()
{
}

}
