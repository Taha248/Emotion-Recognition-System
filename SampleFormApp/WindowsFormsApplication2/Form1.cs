using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApplication2
{
    public partial class Form1 : Form
    {
        public static string DB_HOST = "localhost";
        public static string DB_USER = "root";
        public static string DB_PASSWORD = "";
        public static string DB_NAME = "Emotion_Recognition";
        public static string CONNECTION_STRING = @"server=" + DB_HOST + ";user id = " + DB_USER +
                                  ";password=" + DB_PASSWORD + "; persistsecurityinfo=True;database="
                                               + DB_NAME + ";convert zero datetime=True";
        public static double totalTime = 0;

        public Form1()
        {
            InitializeComponent();
            loadUI();
            fillSampleID();
        }

        private void fillSampleID()
        {
            MySqlConnection conn = new MySqlConnection(CONNECTION_STRING);
            double id = 0;
            try
            {
                String query = "SELECT MAX(sampleID) AS ID FROM samples;";
                MySqlCommand cmd = new MySqlCommand(query,conn);
                conn.Open();
                MySqlDataReader reader = cmd.ExecuteReader();
                if (reader.Read())
                {
                    id = double.Parse(reader["ID"].ToString());
                }
                conn.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                conn.Close();
                txt_sampleID.Text = (id + 1).ToString("0000");
            }
        }

        private void loadUI()
        {

            Dictionary<string, string> genders = new Dictionary<string, string>();
            genders.Add("", "  Select Gender");
            genders.Add("M", "     Male     ");
            genders.Add("F", "     Female    ");

            combo_gender.DataSource = new BindingSource(genders, null);
            combo_gender.DisplayMember = "Value";
            combo_gender.ValueMember = "Key";


            Dictionary<string, string> emotion = new Dictionary<string, string>();


            emotion.Add("0", " Select Emotion");
            emotion.Add("Sad", "     Sad     ");
            emotion.Add("Happy", "     Happy     ");
            emotion.Add("Surprised", "     Surprised     ");
            emotion.Add("Fearful", "     Fearful     ");
            emotion.Add("Excited", "     Excited     ");
            emotion.Add("Disgusted", "     Disgusted     ");
            emotion.Add("Neutral", "     Neutral     ");

            combo_emotions.DataSource = new BindingSource(emotion, null);
            combo_emotions.DisplayMember = "Value";
            combo_emotions.ValueMember = "Key";

        }

        private void panel_form_Paint(object sender, PaintEventArgs e)
        {

        }

        private void btn_form_submit_Click(object sender, EventArgs e)
        {
            timer1.Start();
            createFolder();
            panel2.Visible = true;
            panel_form.Visible = false;
        }

        private void createFolder()
        {
            string path = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            string newPath = "/Samples"+"/"+txt_sampleID.Text+"/"+ ((KeyValuePair<string, string>)combo_emotions.SelectedItem).Key;
            try { 
            if (!Directory.Exists(path + "/"+ newPath))
            {
                Directory.CreateDirectory(path + newPath);
            }
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        private void insertData()
        {
            MySqlConnection conn = new MySqlConnection(CONNECTION_STRING);
            try
            {
                String query = "INSERT INTO samples(sampleID, age, gender, duration, emotion) VALUES('" + txt_sampleID.Text + "', '" + txt_Age.Text + "', '" + ((KeyValuePair<string, string>)combo_gender.SelectedItem).Key + "', "+ totalTime + ", '" + ((KeyValuePair<string, string>)combo_emotions.SelectedItem).Key + "');";
                MySqlCommand cmd = new MySqlCommand(query, conn);
                conn.Open();
                cmd.ExecuteNonQuery();
                conn.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                conn.Close();
                MessageBox.Show("Sample data successfully inserted .", "Successfully Inserted");
            }
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            insertData();
            fillSampleID();
            totalTime = 0;
            timer1.Stop();
            panel_form.Visible = true;
            panel2.Visible = false;



        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            totalTime++;
            TimeSpan t = TimeSpan.FromSeconds(totalTime);
            string answer = string.Format("{1:D2}m:{2:D2}s",
                                    t.Hours,
                                    t.Minutes,
                                    t.Seconds,
                                    t.Milliseconds);

            label7.Text = answer;

        }
    }
}
