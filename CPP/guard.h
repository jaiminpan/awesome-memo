#ifndef _PZM_GUARD_H_
#define _PZM_GUARD_H_

namespace pzm{
namespace Synch{

//scoped locking
template<class LOCK>
class Guard{
public:
    Guard(LOCK& lock):lock_(&lock), own_(false)
    {
        acquire();
    }
    ~Guard()
    {
        release();
    }
    void acquire()
    {
        lock_->acquire();
        own_ = true;
    }
    void release()
    {
        if(own_) {
            own_ = false;
            lock_->release();
        }
    }

private:
    LOCK* lock_;
    bool own_;

    Guard(){}
    Guard(const Guard &){}
    void operator=(const Guard &){}
};

class Lock
{
  public:
      virtual void acquire()=0;
      virtual void release()=0;
};
  
class Null_Lock:public Lock
{
  public:
      virtual void acquire(){};
      virtual void release(){};
};
  
}
}

/* example
#include "Guard.h"
#include "iostream"
using namespace std;

class mutex:public pzm::Synch::Lock
{
public:

    virtual void acquire(){cout<<"lock"<<endl;}
    virtual void release(){cout<<"unlock"<<endl;}
};

int main(int argc, char *argv[]){
    mutex m;
    {
        pzm::Synch::Guard<mutex> guard(m);
    }
    cout<<"end"<<endl;
    return 0;
}
*/

#endif
