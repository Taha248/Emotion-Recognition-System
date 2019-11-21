namespace WindowsFormsApplication2
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.txt_sampleID = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.txt_Age = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.panel_form = new System.Windows.Forms.Panel();
            this.btn_form_submit = new System.Windows.Forms.Button();
            this.combo_emotions = new System.Windows.Forms.ComboBox();
            this.combo_gender = new System.Windows.Forms.ComboBox();
            this.panel2 = new System.Windows.Forms.Panel();
            this.btnStop = new System.Windows.Forms.Button();
            this.label11 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.panel_form.SuspendLayout();
            this.panel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // txt_sampleID
            // 
            this.txt_sampleID.Enabled = false;
            this.txt_sampleID.Location = new System.Drawing.Point(189, 114);
            this.txt_sampleID.Name = "txt_sampleID";
            this.txt_sampleID.Size = new System.Drawing.Size(99, 20);
            this.txt_sampleID.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(110, 117);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(61, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "SampleID";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(110, 167);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(29, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Age";
            // 
            // txt_Age
            // 
            this.txt_Age.Location = new System.Drawing.Point(189, 164);
            this.txt_Age.Name = "txt_Age";
            this.txt_Age.Size = new System.Drawing.Size(99, 20);
            this.txt_Age.TabIndex = 2;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(115, 180);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(0, 13);
            this.label3.TabIndex = 5;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(110, 217);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(48, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "Gender";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 15.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(135, 38);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(139, 25);
            this.label5.TabIndex = 8;
            this.label5.Text = "Sample Form";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(110, 270);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(52, 13);
            this.label6.TabIndex = 9;
            this.label6.Text = "Emotion";
            // 
            // panel_form
            // 
            this.panel_form.Controls.Add(this.btn_form_submit);
            this.panel_form.Controls.Add(this.combo_emotions);
            this.panel_form.Controls.Add(this.combo_gender);
            this.panel_form.Controls.Add(this.label5);
            this.panel_form.Controls.Add(this.label6);
            this.panel_form.Controls.Add(this.txt_sampleID);
            this.panel_form.Controls.Add(this.label1);
            this.panel_form.Controls.Add(this.label4);
            this.panel_form.Controls.Add(this.txt_Age);
            this.panel_form.Controls.Add(this.label3);
            this.panel_form.Controls.Add(this.label2);
            this.panel_form.Location = new System.Drawing.Point(12, 12);
            this.panel_form.Name = "panel_form";
            this.panel_form.Size = new System.Drawing.Size(398, 441);
            this.panel_form.TabIndex = 10;
            this.panel_form.Paint += new System.Windows.Forms.PaintEventHandler(this.panel_form_Paint);
            // 
            // btn_form_submit
            // 
            this.btn_form_submit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(92)))), ((int)(((byte)(184)))), ((int)(((byte)(92)))));
            this.btn_form_submit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_form_submit.ForeColor = System.Drawing.Color.White;
            this.btn_form_submit.Location = new System.Drawing.Point(160, 341);
            this.btn_form_submit.Name = "btn_form_submit";
            this.btn_form_submit.Size = new System.Drawing.Size(75, 23);
            this.btn_form_submit.TabIndex = 12;
            this.btn_form_submit.Text = "Start";
            this.btn_form_submit.UseVisualStyleBackColor = false;
            this.btn_form_submit.Click += new System.EventHandler(this.btn_form_submit_Click);
            // 
            // combo_emotions
            // 
            this.combo_emotions.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.combo_emotions.FormattingEnabled = true;
            this.combo_emotions.Location = new System.Drawing.Point(189, 268);
            this.combo_emotions.Name = "combo_emotions";
            this.combo_emotions.Size = new System.Drawing.Size(99, 21);
            this.combo_emotions.TabIndex = 11;
            // 
            // combo_gender
            // 
            this.combo_gender.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.combo_gender.FormattingEnabled = true;
            this.combo_gender.Location = new System.Drawing.Point(189, 212);
            this.combo_gender.Name = "combo_gender";
            this.combo_gender.Size = new System.Drawing.Size(99, 21);
            this.combo_gender.TabIndex = 10;
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.label7);
            this.panel2.Controls.Add(this.btnStop);
            this.panel2.Controls.Add(this.label11);
            this.panel2.Location = new System.Drawing.Point(15, 12);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(398, 441);
            this.panel2.TabIndex = 11;
            this.panel2.Visible = false;
            // 
            // btnStop
            // 
            this.btnStop.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(217)))), ((int)(((byte)(83)))), ((int)(((byte)(79)))));
            this.btnStop.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnStop.ForeColor = System.Drawing.Color.White;
            this.btnStop.Location = new System.Drawing.Point(161, 333);
            this.btnStop.Name = "btnStop";
            this.btnStop.Size = new System.Drawing.Size(86, 37);
            this.btnStop.TabIndex = 12;
            this.btnStop.Text = "Stop";
            this.btnStop.UseVisualStyleBackColor = false;
            this.btnStop.Click += new System.EventHandler(this.btnStop_Click);
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(115, 180);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(0, 13);
            this.label11.TabIndex = 5;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(129, 154);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(151, 39);
            this.label7.TabIndex = 13;
            this.label7.Text = "00m:00s";
            // 
            // timer1
            // 
            this.timer1.Interval = 1000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(419, 455);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.panel_form);
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Sample Data Collector";
            this.panel_form.ResumeLayout(false);
            this.panel_form.PerformLayout();
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TextBox txt_sampleID;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txt_Age;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Panel panel_form;
        private System.Windows.Forms.Button btn_form_submit;
        private System.Windows.Forms.ComboBox combo_emotions;
        private System.Windows.Forms.ComboBox combo_gender;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Button btnStop;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Timer timer1;
    }
}

