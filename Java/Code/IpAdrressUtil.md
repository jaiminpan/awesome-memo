
Java例子是这样使用的： 
首先在项目中加入maven支持
```  
        <dependency>
            <groupId>com.maxmind.geoip2</groupId>
            <artifactId>geoip2</artifactId>
            <version>2.8.1</version>
        </dependency>
```

通过Request获取IP
```
public class IpAdrressUtil {
    /**
     * 获取Ip地址
     * @param request
     * @return
     */
    private static String getIpAdrress(HttpServletRequest request) {
        String Xip = request.getHeader("X-Real-IP");
        String XFor = request.getHeader("X-Forwarded-For");
        if(StringUtils.isNotEmpty(XFor) && !"unKnown".equalsIgnoreCase(XFor)){
            //多次反向代理后会有多个ip值，第一个ip才是真实ip
            int index = XFor.indexOf(",");
            if(index != -1){
                return XFor.substring(0,index);
            }else{
                return XFor;
            }
        }
        XFor = Xip;
        if(StringUtils.isNotEmpty(XFor) && !"unKnown".equalsIgnoreCase(XFor)){
            return XFor;
        }
        if (StringUtils.isBlank(XFor) || "unknown".equalsIgnoreCase(XFor)) {
            XFor = request.getHeader("Proxy-Client-IP");
        }
        if (StringUtils.isBlank(XFor) || "unknown".equalsIgnoreCase(XFor)) {
            XFor = request.getHeader("WL-Proxy-Client-IP");
        }
        if (StringUtils.isBlank(XFor) || "unknown".equalsIgnoreCase(XFor)) {
            XFor = request.getHeader("HTTP_CLIENT_IP");
        }
        if (StringUtils.isBlank(XFor) || "unknown".equalsIgnoreCase(XFor)) {
            XFor = request.getHeader("HTTP_X_FORWARDED_FOR");
        }
        if (StringUtils.isBlank(XFor) || "unknown".equalsIgnoreCase(XFor)) {
            XFor = request.getRemoteAddr();
        }
        return XFor;
    }
}
```


然后通过GeoLite2查询得到省份、城市
```
public static void main(String[] args) throws Exception{      
      // 创建 GeoLite2 数据库     
      File database = new File("/Users/admin/GeoLite2-City.mmdb");     
      // 读取数据库内容   
      DatabaseReader reader = new DatabaseReader.Builder(database).build();       
      InetAddress ipAddress = InetAddress.getByName("171.108.233.157");     

      // 获取查询结果      
      CityResponse response = reader.city(ipAddress);     

      // 获取国家信息
      Country country = response.getCountry();
      System.out.println(country.getIsoCode());               // 'CN'
      System.out.println(country.getName());                  // 'China'
      System.out.println(country.getNames().get("zh-CN"));    // '中国'

      // 获取省份
      Subdivision subdivision = response.getMostSpecificSubdivision();
      System.out.println(subdivision.getName());   // 'Guangxi Zhuangzu Zizhiqu'
      System.out.println(subdivision.getIsoCode()); // '45'
      System.out.println(subdivision.getNames().get("zh-CN")); // '广西壮族自治区'

      // 获取城市
      City city = response.getCity();
      System.out.println(city.getName()); // 'Nanning'
      Postal postal = response.getPostal();
      System.out.println(postal.getCode()); // 'null'
      System.out.println(city.getNames().get("zh-CN")); // '南宁'
      Location location = response.getLocation();
      System.out.println(location.getLatitude());  // 22.8167
      System.out.println(location.getLongitude()); // 108.3167

}  
```


可以直接创建一个Service
```
import com.maxmind.geoip2.DatabaseReader;
import com.maxmind.geoip2.model.CityResponse;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.File;
import java.net.InetAddress;

/**
 * IP地址服务
 */
@Service
public class IpAddressService {

    private static Logger logger = LoggerFactory.getLogger(IpAddressService.class);

    private static String dbPath = "/usr/local/GeoLite2-City.mmdb";

    private static DatabaseReader reader;

    @Autowired
    private Environment env;

    @PostConstruct
    public void init() {
        try {
            String path = env.getProperty("geolite2.city.db.path");
            if (StringUtils.isNotBlank(path)) {
                dbPath = path;
            }
            File database = new File(dbPath);
            reader = new DatabaseReader.Builder(database).build();
        } catch (Exception e) {
            logger.error("IP地址服务初始化异常:" + e.getMessage(), e);
        }
    }


    public static String getSubdivision(String ipAddress){
        try {
            CityResponse response = reader.city(InetAddress.getByName(ipAddress));
            return response.getMostSpecificSubdivision().getNames().get("zh-CN");
        }catch (Exception e){
            logger.error("根据IP[{}]获取省份失败:{}", ipAddress, e.getMessage());
            return null;
        }
    }
}
```
