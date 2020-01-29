import urllib.request

# In an automated environment the version should be 
# stored in a data file and read at run time to determine the test status.
# This is a quick test with hardcoded data
# Simple if statement to check instead of using assert. 

def test_version():
   version = "v1.0.0"
   url = "http://localhost:5000/version"
   response = urllib.request.urlopen(url)
   rcvd = response.read().decode("utf-8", "strict")
   if rcvd == version :
      print("test_version(): PASSED")
   else:
      print("test_version(): FAILED")


def test_negative():
   # Negative test
   version = "v2.0.0"
   url = "http://localhost:5000/version"
   response = urllib.request.urlopen(url)
   rcvd = response.read().decode("utf-8", "strict")
   if rcvd != version :
      print("test_negative(): PASSED")
   else:
      print("test_negative(): FAILED")

if __name__ == '__main__':
   test_version()
   test_negative()

