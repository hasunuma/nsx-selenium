# nsx-selenium
Multiple access to NSX-T using selenium.

[SeleniumでNSX-T Managerに同時アクセスしてみた！ - FJCT Tech blog](https://tech.fjct.fujitsu.com/entry/selenium-nsx-t)

## How to Use

### setup selenium environment

1. [install openjdk](https://openjdk.org/)
1. [download selenium jar](https://www.selenium.dev/downloads/)
2. [install WebDriver for Chrome](https://chromedriver.chromium.org/downloads)

```
# selenium start
java -jar .\selenium-server-4.15.0.jar standalone

# exec
python3.9 access.py --selenium {selenium_node_IPaddr} --nsx {NSX_T_Manager_IPaddr}
```

## Demo

[![](https://img.youtube.com/vi/qJdpuGoxSso/0.jpg)](https://www.youtube.com/watch?v=qJdpuGoxSso)

