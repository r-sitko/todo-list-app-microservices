#pragma once

#include <memory>

namespace gateway
{

template <typename T>
class ApplicationStarter final
{
public:
  explicit ApplicationStarter(std::unique_ptr<T> pApp)
    : m_pApp{std::move(pApp)}
  {
    m_pApp->init();
    m_pApp->run();
  }
  ~ApplicationStarter()
  {
    m_pApp->deInit();
  }

private:
  std::unique_ptr<T> m_pApp;
};

}
