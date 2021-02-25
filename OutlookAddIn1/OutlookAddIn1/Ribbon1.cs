using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Microsoft.Office.Interop.Outlook;
using Microsoft.Office.Tools.Ribbon;

namespace OutlookAddIn1
{
    public partial class Ribbon1
    {
        private void Ribbon1_Load(object sender, RibbonUIEventArgs e)
        {

        }

        //https://stackoverflow.com/questions/56933847/how-to-show-form-region-button-on-my-ribbon-in-vsto-outlook-c-sharp
        private void button1_Click(object sender, RibbonControlEventArgs e)
        {
            Microsoft.Office.Interop.Outlook.Application oApp = Globals.ThisAddIn.Application;
            NameSpace oNs = oApp.GetNamespace("MAPI");
            MAPIFolder oInbox = oNs.GetDefaultFolder(OlDefaultFolders.olFolderInbox);
            Items oItems = oInbox.Items;
            MailItem oForm = oItems.Add("IPM.Note");
            oForm.Display(false);
            oApp.ActiveInspector().SetCurrentFormPage("OutlookAddIn1.FormRegion1");

        }
    }


}
