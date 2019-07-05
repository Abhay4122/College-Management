from django.db import models

# Create your models here.

class inquery(models.Model):
    inq_id = models.AutoField(primary_key=True)
    inq_nam = models.CharField(max_length=100)
    inq_mail = models.CharField(max_length=50)
    inq_mono = models.CharField(max_length=15)
    inq_subj = models.CharField(max_length=250)
    inq_det = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.inq_nam


class course(models.Model):
    cor_id = models.AutoField(primary_key=True)
    cor_cat = models.CharField(max_length=20)
    cor_nam = models.CharField(max_length=50)
    cor_ful_form = models.CharField(max_length=100)
    cor_dur = models.CharField(max_length=50)
    cor_pak = models.CharField(max_length=10, default='')
    cor_detail = models.CharField(max_length=250)
    cor_syllabus = models.ImageField(upload_to='cit/images', default='')

    def __str__(self):
        return self.cor_nam


class std_registration(models.Model):
    reg_id = models.AutoField(primary_key=True)
    reg_frm_no = models.CharField(max_length=10)
    reg_nam = models.CharField(max_length=50)
    reg_gen = models.CharField(max_length=50)
    reg_fat_nam = models.CharField(max_length=50)
    reg_mot_nam = models.CharField(max_length=50)
    reg_dob = models.DateField()
    reg_location = models.CharField(max_length=150)
    reg_mono = models.CharField(max_length=15)
    reg_fat_mono = models.CharField(max_length=15)
    reg_cat = models.CharField(max_length=50)
    reg_cor = models.CharField(max_length=50)
    reg_psd_cls = models.CharField(max_length=50)
    reg_psd_year = models.IntegerField()
    reg_board = models.CharField(max_length=50)
    reg_gred = models.CharField(max_length=50)
    reg_img = models.ImageField(upload_to='cit/images')
    reg_det = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.reg_nam


class std_exm_marks(models.Model):
    exm_id = models.AutoField(primary_key=True)
    exm_std_id = models.CharField(max_length=10)
    exm_frm_no = models.CharField(max_length=10)
    exm_enroll_no = models.CharField(max_length=20)
    exm_certi_no = models.CharField(max_length=20)
    exm_std_nam = models.CharField(max_length=50)
    exm_fat_nam = models.CharField(max_length=50)
    exm_location = models.CharField(max_length=150)
    exm_cors = models.CharField(max_length=50)
    exm_std_img = models.CharField(max_length=50, default='')
    exm_det = models.DateField()
    exm_award_det = models.DateField()
    exm_session = models.CharField(max_length=50)
    exm_theory = models.CharField(max_length=10)
    exm_prect = models.CharField(max_length=10)
    exm_oral = models.CharField(max_length=10)
    exm_total = models.CharField(max_length=10)

    def __str__(self):
        return self.exm_std_nam


class std_fee(models.Model):
    fee_id = models.AutoField(primary_key=True)
    fee_std_id = models.CharField(max_length=10)
    fee_std_nam = models.CharField(max_length=50)
    fee_fat_nam = models.CharField(max_length=50)
    fee_cors = models.CharField(max_length=50)
    fee_location = models.CharField(max_length=150)
    fee_std_img = models.CharField(max_length=50)
    jan_fee = models.IntegerField(default=0)
    jan_fee_det = models.DateField(null=True, default='')
    feb_fee = models.IntegerField(default=0)
    feb_fee_det = models.DateField(null=True, default='')
    mar_fee = models.IntegerField(default=0)
    mar_fee_det = models.DateField(null=True, default='')
    apr_fee = models.IntegerField(default=0)
    apr_fee_det = models.DateField(null=True, default='')
    may_fee = models.IntegerField(default=0)
    may_fee_det = models.DateField(null=True, default='')
    jun_fee = models.IntegerField(default=0)
    jun_fee_det = models.DateField(null=True, default='')
    jul_fee = models.IntegerField(default=0)
    jul_fee_det = models.DateField(null=True, default='')
    aug_fee = models.IntegerField(default=0)
    aug_fee_det = models.DateField(null=True, default='')
    sep_fee = models.IntegerField(default=0)
    sep_fee_det = models.DateField(null=True, default='')
    oct_fee = models.IntegerField(default=0)
    oct_fee_det = models.DateField(null=True, default='')
    nov_fee = models.IntegerField(default=0)
    nov_fee_det = models.DateField(null=True, default='')
    dec_fee = models.IntegerField(default=0)
    dec_fee_det = models.DateField(null=True, default='')
    total_fee = models.IntegerField(default=0)
    due_fee = models.IntegerField(default=0)

    def __str__(self):
        return self.fee_std_nam