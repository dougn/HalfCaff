import ctypes
import CoreFoundation
import objc
import subprocess
import time


## from http://benden.us/journal/2014/OS-X-Power-Management-No-Sleep-Howto/
##      http://alistra.ghost.io/2015/03/15/making-your-os-x-not-sleep-while-running-scripts/

def SetUpIOFramework():
    # load the IOKit library
    framework = ctypes.cdll.LoadLibrary(
      '/System/Library/Frameworks/IOKit.framework/IOKit')
  
    # declare parameters as described in IOPMLib.h
    framework.IOPMAssertionCreateWithName.argtypes = [
        ctypes.c_void_p,  # CFStringRef
        ctypes.c_uint32,  # IOPMAssertionLevel
        ctypes.c_void_p,  # CFStringRef
        ctypes.POINTER(ctypes.c_uint32)]  # IOPMAssertionID
    framework.IOPMAssertionRelease.argtypes = [
        ctypes.c_uint32]  # IOPMAssertionID
    return framework

def StringToCFString(string):
    # we'll need to convert our strings before use
    return objc.pyobjc_id(
        CoreFoundation.CFStringCreateWithCString(None, string,
            CoreFoundation.kCFStringEncodingASCII).nsstring())

def AssertionCreateWithName(framework, a_type,
                            a_level, a_reason):
    # this method will create an assertion using the IOKit library
    # several parameters
    a_id = ctypes.c_uint32(0)
    a_type = StringToCFString(a_type)
    a_reason = StringToCFString(a_reason)
    a_error = framework.IOPMAssertionCreateWithName(
        a_type, a_level, a_reason, ctypes.byref(a_id))
  
    # we get back a 0 or stderr, along with a unique c_uint
    # representing the assertion ID so we can release it later
    return a_error, a_id

def AssertionRelease(framework, assertion_id):
    # releasing the assertion is easy, and also returns a 0 on
    # success, or stderr otherwise
    return framework.IOPMAssertionRelease(assertion_id)


class Control(object):
    def __init__(self, no_idle='NoIdleSleepAssertion',
                 reason='HalfCaff - VPN live connection'):
        self.no_idle = no_idle
        self.reason = reason
        self.framework = SetUpIOFramework()
        self.a_id = None
        
    def caffeinate(self, no_idle=None, reason=None):
        if not no_idle:
            no_idle = self.no_idle
        if not reason:
            reason = self.reason
        if self.a_id:
            return
        ret, self.a_id = AssertionCreateWithName(
            self.framework, no_idle, 255, reason)
        return ret
    
    def decaffeinate(self):
        if not self.a_id:
            return
        AssertionRelease(self.framework, self.a_id)
        self.a_id = None
        

def main():
    # let's create a no idle assertion for 30 seconds
    no_idle = 'NoIdleSleepAssertion'
    reason = 'Test of Pythonic power assertions'
  
    # first, we'll need the IOKit framework
    framework = SetUpIOFramework()
  
    # next, create the assertion and save the ID!
    ret, a_id = AssertionCreateWithName(framework, no_idle, 255, reason)
    print '\n\nCreating power assertion: status %s, id %s\n\n' % (ret, a_id)
  
    # subprocess a call to pmset to verify the assertion worked
    subprocess.call(['pmset', '-g', 'assertions'])
    time.sleep(5)
  
    # finally, release the assertion of the ID we saved earlier
    AssertionRelease(framework, a_id)
    print '\n\nReleasing power assertion: id %s\n\n' % a_id
  
    # verify the assertion has been removed
    subprocess.call(['pmset', '-g', 'assertions'])

if __name__ == '__main__':
    main()