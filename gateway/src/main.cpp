#include <gateway/applicationstarter.hpp>
#include <gateway/config.hpp>
#include <gateway/exceptionbase.hpp>
#include <gateway/gatewayapp.hpp>
#include <exception>
#include <memory>
#include <thread>
#include <iostream>

int main()
{
  try
  {
    auto pConfig = std::make_unique<gateway::Config>();
    auto pApp = std::make_unique<gateway::GatewayApp>(std::move(pConfig));
    gateway::ApplicationStarter<gateway::GatewayApp> appStarter(std::move(pApp));
  }
  catch (const gateway::ExceptionBase& rEx)
  {
    std::cerr << rEx;
    return EXIT_FAILURE;
  }
  catch (const std::exception& rEx)
  {
    std::cerr
      << "Exception occured: "
      << rEx.what()
      << std::endl;
    return EXIT_FAILURE;
  }
  catch (...)
  {
    std::cerr
      << "Unknown exception occured: "
      << std::endl;
    return EXIT_FAILURE;
  }
}
