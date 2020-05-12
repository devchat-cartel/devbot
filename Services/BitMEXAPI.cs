using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Newtonsoft.Json.Converters;
using System.Dynamic;
using System.Threading.Tasks;
using System.Web;

namespace CartelBotAPI.Services
{
    public class OrderBookItemtest
    {
        public string Symbol { get; set; }
        public int Level { get; set; }
        public int BidSize { get; set; }
        public decimal BidPrice { get; set; }
        public int AskSize { get; set; }
        public decimal AskPrice { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class BitMEXApi
    {
        private const string domain = "https://www.bitmex.com";
		private string apiKey;
		private string apiSecret;
        private int rateLimit;

        public BitMEXApi(string bitmexKey, string bitmexSecret, int rateLimit = 5000)
        {
            this.apiKey = bitmexKey;
            this.apiSecret = bitmexSecret;
            this.rateLimit = rateLimit;
        }

        private string BuildQueryData(Dictionary<string, string> param)
        {
            if (param == null)
                return "";

            StringBuilder b = new StringBuilder();
            foreach (var item in param)
                b.Append(string.Format("&{0}={1}", item.Key, WebUtility.UrlEncode(item.Value)));

            try { return b.ToString().Substring(1); }
            catch (Exception) { return ""; }
        }

        private string BuildJSON(Dictionary<string, string> param)
        {
            if (param == null)
                return "";

            var entries = new List<string>();
            foreach (var item in param)
                entries.Add(string.Format("\"{0}\":\"{1}\"", item.Key, item.Value));

            return "{" + string.Join(",", entries) + "}";
        }

        public static string ByteArrayToString(byte[] ba)
        {
            StringBuilder hex = new StringBuilder(ba.Length * 2);
            foreach (byte b in ba)
                hex.AppendFormat("{0:x2}", b);
            return hex.ToString();
        }

        private long GetExpires()
        {
            return DateTimeOffset.UtcNow.ToUnixTimeSeconds() + 3600; // set expires one hour in the future
        }

        private async Task<string> Query(string method, string function, Dictionary<string, string> param = null, bool auth = false, bool json = false)
        {
            string paramData = json ? BuildJSON(param) : BuildQueryData(param);
            string url = "/api/v1" + function + ((method == "GET" && paramData != "") ? "?" + paramData : "");
            string postData = (method != "GET") ? paramData : "";

            HttpWebRequest webRequest = (HttpWebRequest)WebRequest.Create(domain + url);
            webRequest.Method = method;

            if (auth)
            {
                string expires = GetExpires().ToString();
                string message = method + url + expires + postData;
                byte[] signatureBytes = Hmacsha256(Encoding.UTF8.GetBytes(apiSecret), Encoding.UTF8.GetBytes(message));
                string signatureString = ByteArrayToString(signatureBytes);

                webRequest.Headers.Add("api-expires", expires);
                webRequest.Headers.Add("api-key", apiKey);
                webRequest.Headers.Add("api-signature", signatureString);
            }

            try
            {
                if (postData != "")
                {
                    webRequest.ContentType = json ? "application/json" : "application/x-www-form-urlencoded";
                    var data = Encoding.UTF8.GetBytes(postData);
                    using (var stream = webRequest.GetRequestStream())
                    {
                        stream.Write(data, 0, data.Length);
                    }
                }

                using (WebResponse webResponse = await webRequest.GetResponseAsync())
                using (Stream str = webResponse.GetResponseStream())
                using (StreamReader sr = new StreamReader(str))
                {
                    return await sr.ReadToEndAsync();
                }
            }
            catch (WebException wex)
            {
                using (HttpWebResponse response = (HttpWebResponse)wex.Response)
                {
                    if (response == null)
                        throw;

                    using (Stream str = response.GetResponseStream())
                    {
                        using (StreamReader sr = new StreamReader(str))
                        {
                            return sr.ReadToEnd();
                        }
                    }
                }
            }
        }

        public async Task<string> getOHLC(string symbol)
        {
            //param["filter"] = HttpUtility.UrlEncode("{\"startTime\":" + start + ",\"endTime\":" + end + "}");
            var param = new Dictionary<string, string>();
            param["symbol"] = symbol;
            param["binSize"] = "1h";
            param["count"] = "1";
            param["reverse"] = "true";
            return await Query("GET", "/trade/bucketed", param, true);
        }

        public async Task<string> getPosition(string symbol = "XBTUSD")
        {
            var param = new Dictionary<string, string>();
            param["symbol"] = symbol;
            return await Query("GET", "/position", param, true);
        }

		/*public BitmexBigOrders.PositionItem GetPosition()
		{
			var param = new Dictionary<string, string>();
			param["filter"] = "{\"symbol\":\"XRPZ18\"}";
			string res = Query("GET", "/position", param, true);

			//return JsonConvert.DeserializeObject<BitmexBigOrders.Models.PositionItemList>(res);

			
			return JsonConvert.DeserializeObject<BitmexBigOrders.PositionItem>(res);
			//JsonSerializer j = new JsonSerializer();
		}*/

        //public List<OrderBookItem> GetOrderBook(string symbol, int depth)
        //{
        //    var param = new Dictionary<string, string>();
        //    param["symbol"] = symbol;
        //    param["depth"] = depth.ToString();
        //    string res = Query("GET", "/orderBook", param);
        //    return JsonSerializer.DeserializeFromString<List<OrderBookItem>>(res);
        //}

        //public string GetOrders()
        //{
        //    var param = new Dictionary<string, string>();
        //    param["symbol"] = "XBTUSD";
        //    //param["filter"] = "{\"open\":true}";
        //    //param["columns"] = "";
        //    //param["count"] = 100.ToString();
        //    //param["start"] = 0.ToString();
        //    //param["reverse"] = false.ToString();
        //    //param["startTime"] = "";
        //    //param["endTime"] = "";
        //    return Query("GET", "/order", param, true);
        //}

        //public string PostOrders()
        //{
        //    var param = new Dictionary<string, string>();
        //    param["symbol"] = "XBTUSD";
        //    param["side"] = "Buy";
        //    param["orderQty"] = "1";
        //    param["ordType"] = "Market";
        //    return Query("POST", "/order", param, true);
        //}

        //public string DeleteOrders()
        //{
            ///var param = new Dictionary<string, string>();
            ///param["orderID"] = "de709f12-2f24-9a36-b047-ab0ff090f0bb";
            ///param["text"] = "cancel order by ID";
            ///return Query("DELETE", "/order", param, true, true);
        //}

        private byte[] Hmacsha256(byte[] keyByte, byte[] messageBytes)
        {
            using (var hash = new HMACSHA256(keyByte))
            {
                return hash.ComputeHash(messageBytes);
            }
        }

        #region RateLimiter

        private long lastTicks = 0;
        private object thisLock = new object();

        private void RateLimit()
        {
            lock (thisLock)
            {
                long elapsedTicks = DateTime.Now.Ticks - lastTicks;
                var timespan = new TimeSpan(elapsedTicks);
                if (timespan.TotalMilliseconds < rateLimit)
                    Thread.Sleep(rateLimit - (int)timespan.TotalMilliseconds);
                lastTicks = DateTime.Now.Ticks;
            }
        }

        #endregion RateLimiter
    }
}
