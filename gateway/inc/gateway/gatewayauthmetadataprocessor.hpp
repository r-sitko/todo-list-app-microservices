#pragma once

#include <gateway/config.hpp>
#include <grpcpp/grpcpp.h>
#include <memory>
#include <vector>

namespace gateway
{

class GatewayAuthMetadataProcessor final : public grpc::AuthMetadataProcessor
{
public:
  explicit GatewayAuthMetadataProcessor(std::shared_ptr<gateway::Config> pConfig);
  ~GatewayAuthMetadataProcessor() = default;
  GatewayAuthMetadataProcessor(const GatewayAuthMetadataProcessor&) = delete;
  GatewayAuthMetadataProcessor(GatewayAuthMetadataProcessor&&) = delete;
  GatewayAuthMetadataProcessor& operator=(const GatewayAuthMetadataProcessor&) = delete;
  GatewayAuthMetadataProcessor& operator=(GatewayAuthMetadataProcessor&&) = delete;

  grpc::Status Process(
    const InputMetadata& rAuthMetadata,
    grpc::AuthContext* pContext,
    OutputMetadata* pConsumedAuthMetadata,
    OutputMetadata* pResponseMetadata) final;

  void addMethodToWhiteList(const std::string& rMethodName);

private:
  bool authNeeded(const std::string& rMethodName);

  std::shared_ptr<gateway::Config> m_pConfig;
  std::vector<std::string> m_methodsWhiteList;

  static const std::string m_kPathKey;
  static const std::string m_kAuthKey;
  static const std::string m_kUserTokenKey;
};

}
