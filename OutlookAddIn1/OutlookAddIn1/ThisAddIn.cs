using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Outlook = Microsoft.Office.Interop.Outlook;
using Office = Microsoft.Office.Core;
using System.Windows.Forms;
using System.Net;
using System.IO;
using Newtonsoft.Json;
using System.Runtime.InteropServices;

namespace OutlookAddIn1
{
    public partial class ThisAddIn
    {    
        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            Application.ItemSend += new
                Outlook.ApplicationEvents_11_ItemSendEventHandler(Application_ItemSend);
        }

        void Application_ItemSend(object Item, ref bool Cancel)
        {
            Outlook.MailItem mail = Item as Outlook.MailItem;
            if (mail != null)
            {
                Outlook.Recipients recips = mail.Recipients;

                foreach (Outlook.Recipient recip in recips)
                {
                    string s = "<HTML><BODY>{0}</BODY></HTML>";

                    string addToBody = string.Format(s, GetTrackingCode(mail.SenderEmailAddress, recip.Address).inject_code);

                    if (!mail.HTMLBody.EndsWith(addToBody))
                        mail.HTMLBody += addToBody;
                }


            }
        }

       
        public Response GetTrackingCode(string sender,string receiver)
        {
            string responseHtmlCode = "-1";
            string s = "http://localhost:5000/get_tracking_code_for_email?sender={0}&receiver={1}";
            string url = string.Format(s, sender, receiver);
            // Create a request for the URL.
            WebRequest request = WebRequest.Create(url);
            // If required by the server, set the credentials.
            request.Credentials = CredentialCache.DefaultCredentials;

            // Get the response.
            WebResponse response = request.GetResponse();
            // Display the status.
            Console.WriteLine(((HttpWebResponse)response).StatusDescription);

            Response responseJson = new Response();
            
            if (((HttpWebResponse)response).StatusCode == HttpStatusCode.OK)
            {
                // Get the stream containing content returned by the server.
                // The using block ensures the stream is automatically closed.
                using (Stream dataStream = response.GetResponseStream())
                {
                    // Open the stream using a StreamReader for easy access.
                    StreamReader reader = new StreamReader(dataStream);
                    // Read the content.
                    string responseFromServer = reader.ReadToEnd();
                    // Display the content.
                    responseHtmlCode = responseFromServer;
                    Console.WriteLine(responseFromServer);
                }
                responseJson = JsonConvert.DeserializeObject<Response>(responseHtmlCode);

            }

            // Close the response.
            response.Close();

            return responseJson;
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            // Nota: Outlook ya no genera este evento. Si tiene código que 
            //    se debe ejecutar cuando Outlook se apaga, consulte https://go.microsoft.com/fwlink/?LinkId=506785
        }

        public class Response
        {
            public string status_code
            {
                get;
                set;
            }
            public string inject_code
            {
                get;
                set;
            }

        }

        #region Código generado por VSTO

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InternalStartup()
        {
            this.Startup += new System.EventHandler(ThisAddIn_Startup);
            this.Shutdown += new System.EventHandler(ThisAddIn_Shutdown);
        }
        
        #endregion
    }
}
