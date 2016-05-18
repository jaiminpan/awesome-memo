# 农历-公历转换

#### 1.新建年份編碼表
```
/*將日期轉換成農曆的表*/ 
CREATE TABLE SolarData
(
YearID INTEGER NOT NULL, -- 農曆表
DATA CHAR(7) NOT NULL, -- 農曆年對應的16進制數
DataInt INTEGER NOT NULL -- 農曆年對應的10進制數
);
```

#### 2.为年份編碼表插入數據
```
BEGIN;
INSERT INTO SolarData VALUES(1900, '0x04bd8', 19416);
INSERT INTO SolarData VALUES(1901, '0x04ae0', 19168);
INSERT INTO SolarData VALUES(1902, '0x0a570', 42352);
INSERT INTO SolarData VALUES(1903, '0x054d5', 21717);
INSERT INTO SolarData VALUES(1904, '0x0d260', 53856);
INSERT INTO SolarData VALUES(1905, '0x0d950', 55632);
INSERT INTO SolarData VALUES(1906, '0x16554', 91476);
INSERT INTO SolarData VALUES(1907, '0x056a0', 22176);
INSERT INTO SolarData VALUES(1908, '0x09ad0', 39632);
INSERT INTO SolarData VALUES(1909, '0x055d2', 21970);
INSERT INTO SolarData VALUES(1910, '0x04ae0', 19168);
INSERT INTO SolarData VALUES(1911, '0x0a5b6', 42422);
INSERT INTO SolarData VALUES(1912, '0x0a4d0', 42192);
INSERT INTO SolarData VALUES(1913, '0x0d250', 53840);
INSERT INTO SolarData VALUES(1914, '0x1d255', 119381);
INSERT INTO SolarData VALUES(1915, '0x0b540', 46400);
INSERT INTO SolarData VALUES(1916, '0x0d6a0', 54944);
INSERT INTO SolarData VALUES(1917, '0x0ada2', 44450);
INSERT INTO SolarData VALUES(1918, '0x095b0', 38320);
INSERT INTO SolarData VALUES(1919, '0x14977', 84343);
INSERT INTO SolarData VALUES(1920, '0x04970', 18800);
INSERT INTO SolarData VALUES(1921, '0x0a4b0', 42160);
INSERT INTO SolarData VALUES(1922, '0x0b4b5', 46261);
INSERT INTO SolarData VALUES(1923, '0x06a50', 27216);
INSERT INTO SolarData VALUES(1924, '0x06d40', 27968);
INSERT INTO SolarData VALUES(1925, '0x1ab54', 109396);
INSERT INTO SolarData VALUES(1926, '0x02b60', 11104);
INSERT INTO SolarData VALUES(1927, '0x09570', 38256);
INSERT INTO SolarData VALUES(1928, '0x052f2', 21234);
INSERT INTO SolarData VALUES(1929, '0x04970', 18800);
INSERT INTO SolarData VALUES(1930, '0x06566', 25958);
INSERT INTO SolarData VALUES(1931, '0x0d4a0', 54432);
INSERT INTO SolarData VALUES(1932, '0x0ea50', 59984);
INSERT INTO SolarData VALUES(1933, '0x06e95', 28309);
INSERT INTO SolarData VALUES(1934, '0x05ad0', 23248);
INSERT INTO SolarData VALUES(1935, '0x02b60', 11104);
INSERT INTO SolarData VALUES(1936, '0x186e3', 100067);
INSERT INTO SolarData VALUES(1937, '0x092e0', 37600);
INSERT INTO SolarData VALUES(1938, '0x1c8d7', 116951);
INSERT INTO SolarData VALUES(1939, '0x0c950', 51536);
INSERT INTO SolarData VALUES(1940, '0x0d4a0', 54432);
INSERT INTO SolarData VALUES(1941, '0x1d8a6', 120998);
INSERT INTO SolarData VALUES(1942, '0x0b550', 46416);
INSERT INTO SolarData VALUES(1943, '0x056a0', 22176);
INSERT INTO SolarData VALUES(1944, '0x1a5b4', 107956);
INSERT INTO SolarData VALUES(1945, '0x025d0', 9680);
INSERT INTO SolarData VALUES(1946, '0x092d0', 37584);
INSERT INTO SolarData VALUES(1947, '0x0d2b2', 53938);
INSERT INTO SolarData VALUES(1948, '0x0a950', 43344);
INSERT INTO SolarData VALUES(1949, '0x0b557', 46423);
INSERT INTO SolarData VALUES(1950, '0x06ca0', 27808);
INSERT INTO SolarData VALUES(1951, '0x0b550', 46416);
INSERT INTO SolarData VALUES(1952, '0x15355', 86869);
INSERT INTO SolarData VALUES(1953, '0x04da0', 19872);
INSERT INTO SolarData VALUES(1954, '0x0a5d0', 42448);
INSERT INTO SolarData VALUES(1955, '0x14573', 83315);
INSERT INTO SolarData VALUES(1956, '0x052d0', 21200);
INSERT INTO SolarData VALUES(1957, '0x0a9a8', 43432);
INSERT INTO SolarData VALUES(1958, '0x0e950', 59728);
INSERT INTO SolarData VALUES(1959, '0x06aa0', 27296);
INSERT INTO SolarData VALUES(1960, '0x0aea6', 44710);
INSERT INTO SolarData VALUES(1961, '0x0ab50', 43856);
INSERT INTO SolarData VALUES(1962, '0x04b60', 19296);
INSERT INTO SolarData VALUES(1963, '0x0aae4', 43748);
INSERT INTO SolarData VALUES(1964, '0x0a570', 42352);
INSERT INTO SolarData VALUES(1965, '0x05260', 21088);
INSERT INTO SolarData VALUES(1966, '0x0f263', 62051);
INSERT INTO SolarData VALUES(1967, '0x0d950', 55632);
INSERT INTO SolarData VALUES(1968, '0x05b57', 23383);
INSERT INTO SolarData VALUES(1969, '0x056a0', 22176);
INSERT INTO SolarData VALUES(1970, '0x096d0', 38608);
INSERT INTO SolarData VALUES(1971, '0x04dd5', 19925);
INSERT INTO SolarData VALUES(1972, '0x04ad0', 19152);
INSERT INTO SolarData VALUES(1973, '0x0a4d0', 42192);
INSERT INTO SolarData VALUES(1974, '0x0d4d4', 54484);
INSERT INTO SolarData VALUES(1975, '0x0d250', 53840);
INSERT INTO SolarData VALUES(1976, '0x0d558', 54616);
INSERT INTO SolarData VALUES(1977, '0x0b540', 46400);
INSERT INTO SolarData VALUES(1978, '0x0b5a0', 46496);
INSERT INTO SolarData VALUES(1979, '0x195a6', 103846);
INSERT INTO SolarData VALUES(1980, '0x095b0', 38320);
INSERT INTO SolarData VALUES(1981, '0x049b0', 18864);
INSERT INTO SolarData VALUES(1982, '0x0a974', 43380);
INSERT INTO SolarData VALUES(1983, '0x0a4b0', 42160);
INSERT INTO SolarData VALUES(1984, '0x0b27a', 45690);
INSERT INTO SolarData VALUES(1985, '0x06a50', 27216);
INSERT INTO SolarData VALUES(1986, '0x06d40', 27968);
INSERT INTO SolarData VALUES(1987, '0x0af46', 44870);
INSERT INTO SolarData VALUES(1988, '0x0ab60', 43872);
INSERT INTO SolarData VALUES(1989, '0x09570', 38256);
INSERT INTO SolarData VALUES(1990, '0x04af5', 19189);
INSERT INTO SolarData VALUES(1991, '0x04970', 18800);
INSERT INTO SolarData VALUES(1992, '0x064b0', 25776);
INSERT INTO SolarData VALUES(1993, '0x074a3', 29859);
INSERT INTO SolarData VALUES(1994, '0x0ea50', 59984);
INSERT INTO SolarData VALUES(1995, '0x06b58', 27480);
INSERT INTO SolarData VALUES(1996, '0x055c0', 21952);
INSERT INTO SolarData VALUES(1997, '0x0ab60', 43872);
INSERT INTO SolarData VALUES(1998, '0x096d5', 38613);
INSERT INTO SolarData VALUES(1999, '0x092e0', 37600);
INSERT INTO SolarData VALUES(2000, '0x0c960', 51552);
INSERT INTO SolarData VALUES(2001, '0x0d954', 55636);
INSERT INTO SolarData VALUES(2002, '0x0d4a0', 54432);
INSERT INTO SolarData VALUES(2003, '0x0da50', 55888);
INSERT INTO SolarData VALUES(2004, '0x07552', 30034);
INSERT INTO SolarData VALUES(2005, '0x056a0', 22176);
INSERT INTO SolarData VALUES(2006, '0x0abb7', 43959);
INSERT INTO SolarData VALUES(2007, '0x025d0', 9680);
INSERT INTO SolarData VALUES(2008, '0x092d0', 37584);
INSERT INTO SolarData VALUES(2009, '0x0cab5', 51893);
INSERT INTO SolarData VALUES(2010, '0x0a950', 43344);
INSERT INTO SolarData VALUES(2011, '0x0b4a0', 46240);
INSERT INTO SolarData VALUES(2012, '0x0baa4', 47780);
INSERT INTO SolarData VALUES(2013, '0x0ad50', 44368);
INSERT INTO SolarData VALUES(2014, '0x055d9', 21977);
INSERT INTO SolarData VALUES(2015, '0x04ba0', 19360);
INSERT INTO SolarData VALUES(2016, '0x0a5b0', 42416);
INSERT INTO SolarData VALUES(2017, '0x15176', 86390);
INSERT INTO SolarData VALUES(2018, '0x052b0', 21168);
INSERT INTO SolarData VALUES(2019, '0x0a930', 43312);
INSERT INTO SolarData VALUES(2020, '0x07954', 31060);
INSERT INTO SolarData VALUES(2021, '0x06aa0', 27296);
INSERT INTO SolarData VALUES(2022, '0x0ad50', 44368);
INSERT INTO SolarData VALUES(2023, '0x05b52', 23378);
INSERT INTO SolarData VALUES(2024, '0x04b60', 19296);
INSERT INTO SolarData VALUES(2025, '0x0a6e6', 42726);
INSERT INTO SolarData VALUES(2026, '0x0a4e0', 42208);
INSERT INTO SolarData VALUES(2027, '0x0d260', 53856);
INSERT INTO SolarData VALUES(2028, '0x0ea65', 60005);
INSERT INTO SolarData VALUES(2029, '0x0d530', 54576);
INSERT INTO SolarData VALUES(2030, '0x05aa0', 23200);
INSERT INTO SolarData VALUES(2031, '0x076a3', 30371);
INSERT INTO SolarData VALUES(2032, '0x096d0', 38608);
INSERT INTO SolarData VALUES(2033, '0x04bd7', 19415);
INSERT INTO SolarData VALUES(2034, '0x04ad0', 19152);
INSERT INTO SolarData VALUES(2035, '0x0a4d0', 42192);
INSERT INTO SolarData VALUES(2036, '0x1d0b6', 118966);
INSERT INTO SolarData VALUES(2037, '0x0d250', 53840);
INSERT INTO SolarData VALUES(2038, '0x0d520', 54560);
INSERT INTO SolarData VALUES(2039, '0x0dd45', 56645);
INSERT INTO SolarData VALUES(2040, '0x0b5a0', 46496);
INSERT INTO SolarData VALUES(2041, '0x056d0', 22224);
INSERT INTO SolarData VALUES(2042, '0x055b2', 21938);
INSERT INTO SolarData VALUES(2043, '0x049b0', 18864);
INSERT INTO SolarData VALUES(2044, '0x0a577', 42359);
INSERT INTO SolarData VALUES(2045, '0x0a4b0', 42160);
INSERT INTO SolarData VALUES(2046, '0x0aa50', 43600);
INSERT INTO SolarData VALUES(2047, '0x1b255', 111189);
INSERT INTO SolarData VALUES(2048, '0x06d20', 27936);
INSERT INTO SolarData VALUES(2049, '0x0ada0', 44448);
COMMIT;
```

#### 3、編寫陽曆轉陰曆函數
```
CREATE OR REPLACE FUNCTION f_getNongLi(i_SolarDay DATE) 
RETURN VARCHAR2
  -- 功能：計算陽曆1900/01/31 - 2050/01/22間某一天對應的陰曆是多少
  -- 算法：在一張表中用10進制格式保存某個農曆年每月大小,有無閏月,閏月大小信息
  --           1.用12個2進制位來表示某個農曆年每月的大小，大月記为1，否則为0
  --           2.用低4位來表示閏月的月份，沒有閏月記为0
  --           3.用一個高位表示閏月的大小，閏月大記为0，閏月小或無閏月記为0
  --           4.再將該2進制數轉化为10進制，存入表中
  --       農曆2000年: 0 110010010110 0000 -> 0x0c960 -> 51552
  --       農曆2001年: 0 110110010101 0100 -> 0x0d954 -> 55636
  --       采用查表的方式計算出農曆日期
  -- 作者：Angel_XJW        
  -- 修改：1.
  --       2.
AS
  v_OffSet         INT;
  v_Lunar          INT;          -- 農曆年是否含閏月,幾月是閏月,閏月天數,其它月天數
  v_YearDays       INT;          -- 農曆年所含天數
  v_MonthDays      INT;          -- 農曆月所含天數
  v_LeapMonthDays  INT;          -- 農曆閏月所含天數
  v_LeapMonth      INT;          -- 農曆年閏哪個月 1-12 , 沒閏傳回 0
  v_LeapFlag       INT;          -- 某農曆月是否为閏月  1:是  0:不是
  v_MonthNo        INT;          -- 某農曆月所對應的2進制數 如農曆3月: 001000000000 
  i                INT;
  j                INT; 
  k                INT;
  v_Year           INT;          -- i_SolarDay 對應的農曆年
  v_Month          INT;          -- i_SolarDay 對應的農曆月
  v_Day            INT;          -- i_SolarDay 對應的農曆日
  
  o_OutputDate     VARCHAR2(25); -- 返回值  格式：農曆 ****年 **(閏)月 **日  
  e_ErrMsg         VARCHAR2(200);
  e_ErrDate        EXCEPTION;
BEGIN
   --輸入参數判斷
   IF i_SolarDay<TO_DATE('2000-01-31','YYYY-MM-DD') OR i_SolarDay>=TO_DATE('2050-01-23','YYYY-MM-DD') THEN
     RAISE e_ErrDate;
   END IF ;
 
  -- i_SolarDay 到 1900-01-30(即農曆1900-01-01的前一天) 的天數
  v_OffSet := TRUNC(i_SolarDay, 'DD') - TO_DATE('1900-01-30', 'YYYY-MM-DD');
 
  -- 確定農曆年開始
  i := 1900;
  WHILE i < 2050 AND v_OffSet > 0 LOOP
    v_YearDays := 348;    --  29*12 以每年12個農曆月,每個農曆月含29個農曆日为基數
    v_LeapMonthDays := 0;
    
    -- 取出農曆年是否含閏月,幾月是閏月,閏月天數,其它月天數
    -- 如農曆2001年: 0x0d954(16進制) -> 55636(10進制) -> 0 110110010101 0100(2進制)
    -- 1,2,4,5,8,10,12月大, 3,6,7,9,11月小, 4月为閏月，閏月小
    SELECT DataInt INTO v_Lunar FROM SolarData WHERE YearId = i;
    -- 傳回農曆年的總天數
    j := 32768;            --   100000000000 0000 -> 32768
                           -- 0 110110010101 0100 -> 55636(農曆2001年)
    -- 依次判斷v_Lunar年個月是否为大月，是則加一天 
    WHILE j > 8 LOOP       -- 閏月另行判斷 8 -> 0 000000000000 1000    
      IF BITAND(v_Lunar, j) + 0 > 0 then
        v_YearDays := v_YearDays + 1;
      END IF;
      j := j/2;            -- 判斷下一個月是否为大
    END LOOP;
    -- 傳回農曆年閏哪個月 1-12 , 沒閏傳回 0   15 -> 1 0000
    v_LeapMonth := BITAND(v_Lunar, 15) + 0;
    -- 傳回農曆年閏月的天數 ,加在年的總天數上
    IF v_LeapMonth > 0 THEN
      -- 判斷閏月大小 65536 -> 1 000000000000 0000 
      IF BITAND(v_Lunar, 65536)+0 > 0 THEN
        v_LeapMonthDays := 30;
      ELSE
        v_LeapMonthDays := 29;
      END IF;
      v_YearDays := v_YearDays + v_LeapMonthDays;
    END IF;
    v_OffSet := v_OffSet - v_YearDays;
    i := i + 1;
  END LOOP;
  IF v_OffSet <= 0 THEN
    -- i_SolarDay 在所屬農曆年(即i年)中的第 v_OffSet 天 
    v_OffSet := v_OffSet + v_YearDays;  
    i := i - 1;
  END IF;
  -- 確定農曆年結束
  v_Year := i;
  -- 確定農曆月開始
  i := 1;
  SELECT DataInt INTO v_Lunar FROM SolarData WHERE YearId = v_Year; 
  -- 判斷那個月是润月
  -- 如農曆2001年 (55636,15 -> 0 1101100101010100, 1111 -> 4) 即润4月,且閏月小
  v_LeapMonth := BITAND(v_Lunar, 15) + 0; 
  v_LeapFlag := 0;
 
  WHILE i < 13 AND v_OffSet > 0 LOOP
    -- 判斷是否为閏月
    v_MonthDays := 0;
    IF (v_LeapMonth > 0 AND i = (v_LeapMonth + 1) AND v_LeapFlag = 0) THEN
      -- 是閏月
      i := i - 1;
      k := i;                -- 保存是閏月的時i的值
      v_LeapFlag := 1;
      -- 傳回農曆年閏月的天數
      IF BITAND(v_Lunar, 65536)+0 > 0 THEN
        v_MonthDays := 30;
      ELSE
        v_MonthDays := 29;
      END IF;
      
    ELSE
      -- 不是閏月
      j := 1;
      v_MonthNo := 65536;
      -- 計算 i 月對應的2進制數 如農曆3月: 001000000000
      WHILE j<= i LOOP
        v_MonthNo := v_MonthNo/2;
        j := j + 1;
      END LOOP;
      -- 計算農曆 v_Year 年 i 月的天數
      IF BITAND(v_Lunar, v_MonthNo)+0 > 0 THEN
        v_MonthDays := 30;
      ELSE
        v_MonthDays := 29;
      END IF;
    END IF;
 
    -- 解除閏月
    IF v_LeapFlag = 1 AND i = v_LeapMonth +1 THEN
      v_LeapFlag := 0;
    END IF;
    v_OffSet := v_OffSet - v_MonthDays;
    i := i + 1;
  END LOOP;
 
  IF v_OffSet <= 0 THEN
    -- i_SolarDay 在所屬農曆月(即i月)中的第 v_OffSet 天 
    v_OffSet := v_OffSet + v_MonthDays;
    i := i - 1;
  END IF;
 
  -- 確定農曆月結束
  v_Month := i;
 
  -- 確定農曆日結束
  v_Day := v_OffSet;
 
  -- 格式化返回值
  o_OutputDate := TO_CHAR(v_Year);
  IF k = i THEN
     o_OutputDate := o_OutputDate || LPAD(TO_CHAR(v_Month), 2, '0');
  ELSE
     o_OutputDate := o_OutputDate || LPAD(TO_CHAR(v_Month), 2, '0');
  END IF;
  o_OutputDate := o_OutputDate || LPAD(TO_CHAR(v_Day), 2, '0');
  RETURN o_OutputDate;
EXCEPTION
  WHEN e_Errdate THEN
    RETURN '日期錯誤! 有效範圍(陽曆): 1900/01/31 - 2050/01/22';
  WHEN OTHERS THEN
    e_ErrMsg :=SUBSTR(SQLERRM,1,200);
    RETURN e_ErrMsg;
END;
```
