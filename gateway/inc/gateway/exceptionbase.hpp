#pragma once

#include <exception>
#include <string>
#include <ostream>

#define thrower_2(type, msg) throw type(msg, __FILE__, __LINE__, __func__)
#define thrower_1(type) throw type(__FILE__, __LINE__, __func__)

#define GET_MACRO(_1, _2, NAME, ...) NAME
#define thrower(...) GET_MACRO(__VA_ARGS__, thrower_2, thrower_1, x) (__VA_ARGS__)

namespace gateway
{

class ExceptionBase : public std::exception
{
public:
  explicit ExceptionBase(std::string msg, std::string file, int line, std::string func)
    : m_msg{std::move(msg)},
    m_file{std::move(file)},
    m_line{line},
    m_func{std::move(func)}
  {
  }
  ~ExceptionBase() = default;
  ExceptionBase(const ExceptionBase&) = delete;
  ExceptionBase(ExceptionBase&&) = delete;
  ExceptionBase& operator=(const ExceptionBase&) = delete;
  ExceptionBase& operator=(ExceptionBase&&) = delete;

  const char* what() const noexcept override { return m_msg.c_str(); }
  const char* file() const { return m_file.c_str(); }
  int line() const { return m_line; }
  const char* func() const { return m_func.c_str(); }

  virtual void print(std::ostream& os) const
  {
    os << "Exception occured: "
      << m_msg
      << " "
      << m_file
      << " "
      << m_func
      << " "
      << m_line
      << std::endl;
  }

  friend std::ostream& operator<<(std::ostream& os, const ExceptionBase& rEx)
  {
    rEx.print(os);
    return os;
  }

private:
  const std::string m_msg;
  const std::string m_file;
  const int m_line;
  const std::string m_func;
};

}
