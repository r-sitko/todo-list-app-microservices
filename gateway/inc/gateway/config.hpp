#pragma once

#include <gateway/exceptionbase.hpp>
#include <string>
#include <sstream>

namespace gateway
{

class Config final
{
public:
  Config() = default;
  ~Config() = default;
  Config(const Config&) = delete;
  Config(Config&&) = delete;
  Config& operator=(const Config&) = delete;
  Config& operator=(Config&&) = delete;

  void readConfiguration();
  const std::string& getServiceName() const { return m_serviceName; }
  uint32_t getServicePort() const { return m_servicePort; }
  const std::string& getToDoServiceName() const { return m_todoServiceName; }
  uint32_t getToDoServicePort() const { return m_todoServicePort; }
  const std::string& getUserServiceName() const { return m_userServiceName; }
  uint32_t getUserServicePort() const { return m_userServicePort; }
  const std::string& getServerCert() const { return m_serverCert; }
  const std::string& getServerPrivateKey() const { return m_serverPrivateKey; }
  const std::string& getJwtPrivateKey() const { return m_jwtPrivateKey; }
  const std::string& getJwtPublicKey() const { return m_jwtPublicKey; }

  template <typename T>
  T convertTo(const std::string& rStr) const;

private:
  std::string getFile(const std::string& rFileName);
  std::string getEnv(const std::string& rName);

  std::string m_serviceName;
  uint32_t m_servicePort;
  std::string m_todoServiceName;
  uint32_t m_todoServicePort;
  std::string m_userServiceName;
  uint32_t m_userServicePort;
  std::string m_certFolder;
  std::string m_serverPrivateKeyFile;
  std::string m_serverCertFile;
  std::string m_serverPrivateKey;
  std::string m_serverCert;
  std::string m_jwtPrivateKeyFile;
  std::string m_jwtPublicKeyFile;
  std::string m_jwtPrivateKey;
  std::string m_jwtPublicKey;
};

template <typename T>
T Config::convertTo(const std::string& rStr) const
{
  std::istringstream ss(rStr);
  T ret;
  ss >> ret;
  return ret;
}

class NoEnvironmentVariable : public ExceptionBase
{
public:
  explicit NoEnvironmentVariable(
    std::string msg,
    std::string file,
    int line,
    std::string func)
    : ExceptionBase(
        std::move("No environment variable found: " + msg),
        std::move(file), line,
        std::move(func))
    {
    }
};

class FileOpenProblem : public ExceptionBase
{
public:
  explicit FileOpenProblem(
    std::string msg,
    std::string file,
    int line,
    std::string func)
    : ExceptionBase(
        std::move("Failed to open file: " + msg),
        std::move(file), line,
        std::move(func))
    {
    }
};

}
