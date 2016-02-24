using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Net;

namespace test_api2
{
  class Program
  {
    static void Main(string[] args)
    {

    string server_url = @"baseride.com",
           https_server_url = @"https://" + server_url,
           http_server_url = @"http://" + server_url,
           login = "login", // enter your login here
           password = "password", // enter your password here
           client_id = "client", // enter your client code here
           client_secret = "secret"; // enter your client secret code here

            HttpWebRequest  request = (HttpWebRequest)WebRequest.Create (
              https_server_url+@"/oauth2/authorize/?response_type=code&client_id="+client_id);
            NetworkCredential myCred = new NetworkCredential(login,password);
            CredentialCache myCache = new CredentialCache();
            myCache.Add(new Uri(https_server_url), "Basic", myCred);
            request.Credentials = myCache;

            string credentials = Convert.ToBase64String(Encoding.ASCII.GetBytes(login + ":" + password));
            request.Headers[HttpRequestHeader.Authorization] = string.Format("Basic {0}", credentials);
            request.AllowAutoRedirect=false;

            HttpWebResponse response = (HttpWebResponse)(request.GetResponse ());
            Console.WriteLine (response.StatusCode );
            if(response.StatusCode != HttpStatusCode.Found || response.Headers["Location"] == null)
             {
              Console.WriteLine ("Error");
              return;
             }
            string loc = response.Headers["Location"];
            response.Close ();

            string [] s = loc.Split('=');
            string code = s[1];
          
            request = (HttpWebRequest)WebRequest.Create(
                  https_server_url + @"/oauth2/token/?callback=call_back&client_id=" + client_id + @"&client_secret=" + client_secret +
                  "&code=" + code + @"&grant_type=authorization_code&redirect_uri=" + http_server_url );
            request.AllowAutoRedirect=false;  

            response = (HttpWebResponse)(request.GetResponse ());

            if(response.StatusCode != HttpStatusCode.OK)
             {
              Console.WriteLine ("Error");
              return;
             }

            Stream dataStream = response.GetResponseStream ();
            StreamReader reader = new StreamReader (dataStream);
            string responseFromServer = reader.ReadToEnd ();

            reader.Close ();
            response.Close ();

            s = responseFromServer.Split(new string[] { "access_token\": \"" }, StringSplitOptions.None);
            s = s[1].Split('\"');

            // custom api calls:

            int vehicle_id = 29687;  
            request = (HttpWebRequest)WebRequest.Create(
              https_server_url+@"/api/v2/profile/whoami/?format=json" // info about user
              //https_server_url+@"/api/v2/transport/vehicle/"+vehicle_id+@"/?format=json" // info about vehicle 29687 
              );
            request.Headers[HttpRequestHeader.Authorization] = string.Format("BEARER {0}", s[0]);
            
            response = (HttpWebResponse)(request.GetResponse ());

            dataStream = response.GetResponseStream ();
            reader = new StreamReader (dataStream);
            responseFromServer = reader.ReadToEnd ();
            reader.Close ();
            response.Close ();

            // result json:

            Console.WriteLine (responseFromServer);
            Console.ReadLine();
    }
  }
}
