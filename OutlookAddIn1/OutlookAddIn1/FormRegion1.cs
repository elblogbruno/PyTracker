using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Office = Microsoft.Office.Core;
using Outlook = Microsoft.Office.Interop.Outlook;

namespace OutlookAddIn1
{
    partial class FormRegion1
    {
       
        #region Generador de áreas de formulario 

        [Microsoft.Office.Tools.Outlook.FormRegionMessageClass(Microsoft.Office.Tools.Outlook.FormRegionMessageClassAttribute.Note)]
        [Microsoft.Office.Tools.Outlook.FormRegionName("OutlookAddIn1.FormRegion1")]
        public partial class FormRegion1Factory
        {
            // Tiene lugar antes de inicializar el área del formulario.
            // Para impedir que aparezca el área del formulario, establezca e.Cancel en true.
            // Use e.OutlookItem para obtener una referencia al elemento de Outlook actual.
            private void FormRegion1Factory_FormRegionInitializing(object sender, Microsoft.Office.Tools.Outlook.FormRegionInitializingEventArgs e)
            {
            }
        }

        #endregion

        // Tiene lugar antes de que se muestre el área del formulario.
        // Use this.OutlookItem para obtener una referencia al elemento de Outlook actual.
        // Use this.OutlookFormRegion para obtener una referencia al área del formulario.
        private void FormRegion1_FormRegionShowing(object sender, System.EventArgs e)
        {
        }

        // Tiene lugar cuando se cierra el área del formulario.
        // Use this.OutlookItem para obtener una referencia al elemento de Outlook actual.
        // Use this.OutlookFormRegion para obtener una referencia al área del formulario.
        private void FormRegion1_FormRegionClosed(object sender, System.EventArgs e)
        {
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Properties.Settings.Default.server_url = "http://95.111.245.169:5000/";
            Properties.Settings.Default.Save();

            MessageBox.Show("Saved settings: " + Properties.Settings.Default.server_url);
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
    }
}
