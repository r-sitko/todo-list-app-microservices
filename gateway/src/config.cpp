#include <gateway/config.hpp>
#include <cstdlib>
#include <fstream>

namespace gateway
{

void Config::readConfiguration()
{
  m_serviceName = getEnv("SERVICE_NAME");
  m_servicePort = convertTo<uint32_t>(getEnv("SERVICE_PORT"));
  m_todoServiceName = getEnv("TODO_SERVICE_NAME");
  m_todoServicePort = convertTo<uint32_t>(getEnv("TODO_SERVICE_PORT"));
  m_userServiceName = getEnv("USER_SERVICE_NAME");
  m_userServicePort = convertTo<uint32_t>(getEnv("USER_SERVICE_PORT"));
  m_certFolder = getEnv("CERT_FOLDER");
  m_serverCertFile = getEnv("SERVER_CERT_FILE");
  m_serverPrivateKeyFile = getEnv("SERVER_PRIVATE_KEY_FILE");
  m_serverCert = getFile(m_certFolder + "/" + m_serverCertFile);
  m_serverPrivateKey = getFile(m_certFolder + "/" + m_serverPrivateKeyFile);
  m_jwtPrivateKeyFile = getEnv("JWT_PRIVATE_KEY_FILE");
  m_jwtPublicKeyFile = getEnv("JWT_PUBLIC_KEY_FILE");
  m_jwtPrivateKey = getFile(m_certFolder + "/" + m_jwtPrivateKeyFile);
  m_jwtPublicKey = getFile(m_certFolder + "/" + m_jwtPublicKeyFile);
}

std::string Config::getFile(const std::string& rFileName)
{
  std::string data;
  std::ifstream file(rFileName, std::ios::in);
  if (file.is_open())
  {
    std::stringstream ss;
    ss << file.rdbuf();
    file.close();
    data = ss.str();
  }
  else
  {
    thrower(FileOpenProblem, rFileName);
  }

  return data;
}

std::string Config::getEnv(const std::string& rName)
{
  char* pValue = std::getenv(rName.c_str());
  if (!pValue)
  {
    thrower(NoEnvironmentVariable, rName);
  }
  return pValue;
}

}
