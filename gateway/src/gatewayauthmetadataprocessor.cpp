#include <gateway/gatewayauthmetadataprocessor.hpp>
#include <jwt-cpp/jwt.h>

namespace gateway
{

const std::string GatewayAuthMetadataProcessor::m_kPathKey{":path"};
const std::string GatewayAuthMetadataProcessor::m_kAuthKey{"authorization"};
const std::string GatewayAuthMetadataProcessor::m_kUserTokenKey{"user-token"};

GatewayAuthMetadataProcessor::GatewayAuthMetadataProcessor(std::shared_ptr<gateway::Config> pConfig)
  : m_pConfig{pConfig}
{
}

grpc::Status GatewayAuthMetadataProcessor::Process(
  const InputMetadata& rAuthMetadata,
  grpc::AuthContext* pContext,
  OutputMetadata* pConsumedAuthMetadata,
  OutputMetadata* pResponseMetadata)
{
  (void)pResponseMetadata;

  auto methodIt = rAuthMetadata.find(m_kPathKey);
  if (methodIt == rAuthMetadata.end())
  {
    return grpc::Status(grpc::StatusCode::INTERNAL, "Internal Error");
  }

  auto methodName = std::string(methodIt->second.cbegin(), methodIt->second.cend());

  if (!authNeeded(methodName))
  {
    return grpc::Status::OK;
  }

  auto tokenIt = rAuthMetadata.find(m_kAuthKey);
  if (tokenIt == rAuthMetadata.end())
  {
    return grpc::Status(grpc::StatusCode::UNAUTHENTICATED, "Missing Token");
  }

  auto token = std::string(tokenIt->second.cbegin(), tokenIt->second.cend());

  try
  {
    auto decodedToken = jwt::decode(token);
    jwt::verify()
      .allow_algorithm(jwt::algorithm::rs256{m_pConfig->getJwtPublicKey()})
      .verify(decodedToken);
  }
  catch (const std::invalid_argument&)
  {
    return grpc::Status(
      grpc::StatusCode::UNAUTHENTICATED,
      std::string("Token verification error"));
  }
  catch (const jwt::token_verification_exception&)
  {
    return grpc::Status(
      grpc::StatusCode::UNAUTHENTICATED,
      std::string("Token verification error"));
  }

  pContext->AddProperty(m_kUserTokenKey, token);
  pContext->SetPeerIdentityPropertyName(m_kUserTokenKey);
  pConsumedAuthMetadata->insert(std::make_pair(m_kUserTokenKey, token));

  return grpc::Status::OK;
}

void GatewayAuthMetadataProcessor::addMethodToWhiteList(const std::string& rMethodName)
{
  if (std::find(m_methodsWhiteList.begin(), m_methodsWhiteList.end(), rMethodName) == m_methodsWhiteList.end())
  {
    m_methodsWhiteList.push_back(rMethodName);
  }
}

bool GatewayAuthMetadataProcessor::authNeeded(const std::string& rMethodName)
{
  auto whiteListIt = std::find(m_methodsWhiteList.begin(), m_methodsWhiteList.end(), rMethodName);
  return m_methodsWhiteList.end() == whiteListIt;
}

}
