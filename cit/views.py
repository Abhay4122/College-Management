from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import inquery, course, std_registration, std_exm_marks, std_fee
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from datetime import date
from django.core import serializers
import json

# Create your views here.
def index(request):
    # Sessions work as global variable in add_fee fee function
    request.session['fee_cors'] = ''
    request.session['fee_nam'] = ''
    return render(request, 'cit/index.html')


def about(request):
    return render(request, 'cit/about.html')


def contact(request):
    return render(request, 'cit/contact.html')


def usr_reg(request):
    # get registrsion form fields from index.html
    f_nam = request.POST.get('reg_f_nam', '')
    l_nam = request.POST.get('reg_l_nam', '')
    e_mail = request.POST.get('reg_mail', '')
    repass_word = request.POST.get('reg_repwd', '')
    if User.username == e_mail:
        return render(request, 'cit/index.html', {'flag_reg' : False})
    else:
        User.objects.create_user(username = e_mail, first_name = f_nam, last_name = l_nam, email = e_mail, password = repass_word)
        return render(request, 'cit/index.html', {'flag_reg' : True})


def usr_inq(request):
    i_nam = request.POST.get('inq_nam', '')
    i_mail = request.POST.get('inq_mail', '')
    i_mono = request.POST.get('inq_mono', '')
    i_subj = request.POST.get('inq_topic', '')
    inq_uery = inquery(inq_nam=i_nam, inq_mail=i_mail, inq_mono=i_mono, inq_subj=i_subj, inq_det=date.today())
    inq_uery.save()
    return render(request, 'cit/index.html', {'flag_inq' : True})


def usr_login(request):
    login_usr = request.POST.get('lgin_unam', '')
    login_pwd = request.POST.get('lgin_pwd', '')
    user = authenticate(username=login_usr, password=login_pwd)
    if user:
        request.session['cit_user'] = login_usr
        user_nam = User.objects.filter(username=login_usr)
        return render(request, 'cit/das_basic.html', {'login_success' : True, 'user_info' : user_nam[0]})
    else:
        return render(request, 'cit/index.html', {'login_feliour' : False})


def dashboard(request):
    if request.session.has_key('cit_user'):
        totl_cor = 0; totl_std = 0; totl_inq = 0
        for i in course.objects.all():
            totl_cor += 1
        for j in std_registration.objects.all():
            totl_std += 1
        for k in inquery.objects.all():
            totl_inq += 1
        return render(request, 'cit/dashboard.html', {'totl_cor' : totl_cor, 'totl_std' : totl_std, 'totl_inq' : totl_inq})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def admin(request):
    if request.session.has_key('cit_user'):
        return render(request, 'cit/das_basic.html')
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def enqu(request):
    if request.session.has_key('cit_user'):
        all_inq = inquery.objects.all()
        return render(request, 'cit/enqu.html', {'all_inq' : all_inq})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def cou_rse(request):
    if request.session.has_key('cit_user'):
        all_cors = course.objects.all().order_by('-cor_id')
        return render(request, 'cit/course.html', {'course' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def add_course(request):
    save_type = request.POST.get('cor_hid')
    cor_cat = request.POST.get('cor_cat', '').lower()
    cor_nam = request.POST.get('cor_nam', '').lower()
    cor_ful_frm = request.POST.get('cor_ful_frm', '').lower()
    cor_dur = request.POST.get('cor_dur', '')
    cor_dit = request.POST.get('cor_dit', '')
    cor_pak = request.POST.get('cor_pak', '')
    cor_syllabus = request.FILES.get('cor_syllabus', '')
    if save_type == 'add':
        if course.objects.filter(cor_nam=cor_nam).exists():
            pass
        else:
            course.objects.get_or_create(cor_cat=cor_cat, cor_nam=cor_nam, cor_ful_form=cor_ful_frm, cor_dur=cor_dur, cor_pak=cor_pak, cor_detail=cor_dit, cor_syllabus=cor_syllabus)
            return render(request, 'cit/course.html')
    elif save_type == 'upd':
        cors_id = request.POST.get('cor_id')
        course.objects.filter(cor_id=cors_id).update(cor_cat=cor_cat, cor_nam=cor_nam, cor_ful_form=cor_ful_frm, cor_dur=cor_dur, cor_pak=cor_pak, cor_detail=cor_dit)
        return render(request, 'cit/course.html')#, {'cors_update_success' : True})


def update_cors(request, cors_id):
    if request.session.has_key('cit_user'):
        cors_detail = course.objects.filter(cor_id=cors_id)
        return render(request, 'cit/update_cors.html', {'cors_detail' : cors_detail})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def del_cors(request, cors_id):
    course.objects.filter(cor_id=cors_id).delete()
    return render(request, 'cit/std_list.html/')#, {'cors_del_success' : True})


def std_reg(request):
    if request.session.has_key('cit_user'):
        all_cors = course.objects.all()
        return render(request, 'cit/std_reg.html', {'course' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def add_std(request):
    save_type = request.POST.get('std_hid')
    std_frm_no = request.POST.get('std_form_num', '')
    std_nam = request.POST.get('std_nam', '').lower()
    std_gender = request.POST.get('std_gen', '').lower()
    std_fat_nam = request.POST.get('std_fat_nam', '').lower()
    std_mot_nam = request.POST.get('std_mot_nam', '').lower()
    std_dob = request.POST.get('std_dob', '')
    std_location = request.POST.get('std_location', '')
    std_mono = request.POST.get('std_mono', '')
    std_fat_mono = request.POST.get('std_fat_mono', '')
    std_category = request.POST.get('std_cat', '').lower()
    std_course = request.POST.get('std_cor', '').lower()
    std_lst_psd_cls = request.POST.get('std_lst_psd_cls', '')
    std_psd_year = request.POST.get('std_psd_year', '')
    std_board = request.POST.get('std_bord', '')
    std_gred = request.POST.get('std_gred', '')
    std_img = request.FILES.get('std_img', '')
    if save_type == 'add':
        if std_registration.objects.filter(reg_nam=std_nam).exists():
            pass
        else:
            reg_std = std_registration(reg_frm_no=std_frm_no, reg_nam=std_nam, reg_gen=std_gender, reg_fat_nam=std_fat_nam, reg_mot_nam=std_mot_nam, reg_dob=std_dob, reg_location=std_location, reg_mono=std_mono, reg_fat_mono=std_fat_mono, reg_cat=std_category, reg_cor=std_course, reg_psd_cls=std_lst_psd_cls, reg_psd_year=std_psd_year, reg_board=std_board, reg_gred=std_gred, reg_img=std_img, reg_det=date.today())
            reg_std.save()
            return render(request, 'cit/std_reg.html')#, {'flag_std_reg' : True})
    else:
        std_id = request.POST.get('std_id')
        std_registration.objects.filter(reg_id=std_id).update(reg_frm_no=std_frm_no, reg_nam=std_nam, reg_gen=std_gender, reg_fat_nam=std_fat_nam, reg_mot_nam=std_mot_nam, reg_location=std_location, reg_mono=std_mono, reg_fat_mono=std_fat_mono, reg_cat=std_category, reg_cor=std_course, reg_psd_cls=std_lst_psd_cls, reg_psd_year=std_psd_year, reg_board=std_board, reg_gred=std_gred)
        return render(request, 'cit/std_list.html/')#, {'std_update_success' : True})


def std_list(request, std_dit):
    if request.session.has_key('cit_user'):
        all_std = std_registration.objects.all().order_by('-reg_id')
        all_cors = course.objects.all()
        inpt_nam = list(std_registration.objects.all())
        for i in inpt_nam:
            sel_nam = str(i).split(' ', 1)[0]
            if sel_nam.lower() == std_dit.lower():
                all_std = std_registration.objects.filter(reg_nam=str(i))
                return render(request, 'cit/std_list.html', {'std' : all_std, 'all_cors' : all_cors})

        if std_registration.objects.filter(reg_cor=std_dit.lower()).exists():
            all_std = std_registration.objects.filter(reg_cor=std_dit.lower())
        elif std_registration.objects.filter(reg_nam=std_dit.lower()).exists():
            all_std = std_registration.objects.filter(reg_nam=std_dit.lower())
        elif std_dit != 'non':
            all_std = ''
        return render(request, 'cit/std_list.html', {'std' : all_std, 'all_cors' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def std_view(request, std_id):
    if request.session.has_key('cit_user'):
        std_detail = std_registration.objects.filter(reg_id=std_id)
        return render(request, 'cit/std_view.html', {'std_detail' : std_detail})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def update_std(request, std_id):
    if request.session.has_key('cit_user'):
        std_detail = std_registration.objects.filter(reg_id=std_id)
        all_cors = course.objects.all()
        return render(request, 'cit/update_std.html', {'std_detail' : std_detail, 'all_cors' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def del_std(request, std_id):
    std_registration.objects.filter(reg_id=std_id).delete()
    return render(request, 'cit/std_list.html/', {'std_del_success' : True})


def add_marks(request, std_dt):
    if request.session.has_key('cit_user'):
        all_cors = course.objects.all()
        if std_registration.objects.filter(reg_cor=std_dt.lower()).exists():
            request.session['fee_cors'] = std_dt
            all_std = std_registration.objects.filter(reg_cor=std_dt.lower())
            data = serializers.serialize('json', all_std)
            return HttpResponse(data, content_type="application/json")
            
        if std_registration.objects.filter(reg_nam=std_dt.lower()).exists():
            request.session['fee_nam'] = std_dt
            std_fat = std_registration.objects.filter(reg_nam=std_dt.lower())
            data = serializers.serialize('json', std_fat)
            return HttpResponse(data, content_type="application/json")
        
        if std_registration.objects.filter(reg_cor=request.session['fee_cors']) and std_registration.objects.filter(reg_nam=request.session['fee_nam']) and std_registration.objects.filter(reg_fat_nam=std_dt):
            all_std = std_registration.objects.filter(reg_cor=request.session['fee_cors']).filter(reg_nam=request.session['fee_nam']).filter(reg_fat_nam=std_dt)
            data = serializers.serialize('json', all_std)
            return HttpResponse(data, content_type="application/json")

        return render(request, 'cit/exam_marks.html', {'all_cors' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def marks(request):
    if request.session.has_key('cit_user'):
        save_typ = request.POST.get('exm_hid', '')
        exm_std_id = request.POST.get('exm_std_id', '')
        exm_std_img = request.POST.get('exm_std_img', '')
        exm_std_nam = request.POST.get('exm_std_nam', '')
        exm_std_fat = request.POST.get('exm_std_fat', '')
        exm_reg_num = request.POST.get('exm_reg_num', '')
        exm_location = request.POST.get('exm_location', '')
        exm_std_cors = request.POST.get('exm_std_cors', '')
        exm_enroll = request.POST.get('exm_enroll', '')
        exm_certi = request.POST.get('exm_certi', '')
        exm_det = request.POST.get('exm_det', '')
        exm_award_det = request.POST.get('exm_award_det', '')
        exm_session = request.POST.get('exm_session', '')
        exm_theory = request.POST.get('exm_theory', '')
        exm_prect = request.POST.get('exm_prect', '')
        exm_oral = request.POST.get('exm_oral', '')
        total = int(exm_theory) + int(exm_prect) + int(exm_oral)
        if save_typ == 'add':
            if std_exm_marks.objects.filter(exm_std_nam=exm_std_nam) and std_exm_marks.objects.filter(exm_fat_nam=exm_std_fat):
                pass
            else:
                std_exm_marks.objects.create(exm_std_img=exm_std_img, exm_std_id=exm_std_id, exm_frm_no=exm_reg_num, exm_enroll_no=exm_enroll, exm_certi_no=exm_certi, exm_std_nam=exm_std_nam, exm_fat_nam=exm_std_fat, exm_location=exm_location, exm_cors=exm_std_cors, exm_det=exm_det, exm_award_det=exm_award_det, exm_session=exm_session, exm_theory=exm_theory, exm_prect=exm_prect, exm_oral=exm_oral, exm_total=total)
                return render(request, 'cit/exam_marks.html')#, {'exm_add_success' : True})
        else:
            exm_id = request.POST.get('exm_id', '')
            std_exm_marks.objects.filter(exm_id=exm_id).update(exm_enroll_no=exm_enroll, exm_certi_no=exm_certi, exm_det=exm_det, exm_award_det=exm_award_det, exm_session=exm_session, exm_theory=exm_theory, exm_prect=exm_prect, exm_oral=exm_oral, exm_total=total)
            return render(request, 'cit/result_list.html', {'exm_upd_success' : True})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def result_list(request):
    if request.session.has_key('cit_user'):
        all_marks = std_exm_marks.objects.all()
        all_cors = course.objects.all()
        std_cors = request.POST.get('std_cors', '')
        std_nam = request.POST.get('std_nam', '')
        if std_cors != '':
            all_marks = std_exm_marks.objects.filter(exm_cors=std_cors)
        if std_nam != '':
            all_marks = std_exm_marks.objects.filter(exm_std_nam=std_nam.title())
        return render(request, 'cit/result_list.html', {'all_marks' : all_marks, 'all_cors' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def result_view(request, exm_id):
    if request.session.has_key('cit_user'):
        exm_detail = std_exm_marks.objects.filter(exm_id=exm_id)
        return render(request, 'cit/exam_view.html', {'exm_detail' : exm_detail})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def update_marks(request, exm_id):
    if request.session.has_key('cit_user'):
        exm_detail = std_exm_marks.objects.filter(exm_id=exm_id)
        return render(request, 'cit/update_marks.html', {'exm_detail' : exm_detail})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def view_cretificate(request):
    if request.session.has_key('cit_user'):
        return render(request, 'cit/view_certi.html')
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def add_fee(request, std_dt):
    if request.session.has_key('cit_user'):
        all_cors = course.objects.all()
        if std_registration.objects.filter(reg_cor=std_dt.lower()).exists():
            request.session['fee_cors'] = std_dt
            all_std = std_registration.objects.filter(reg_cor=std_dt.lower())
            data = serializers.serialize('json', all_std)
            return HttpResponse(data, content_type="application/json")
            
        if std_registration.objects.filter(reg_nam=std_dt.lower()).exists():
            request.session['fee_nam'] = std_dt
            std_fat = std_registration.objects.filter(reg_nam=std_dt.lower())
            data = serializers.serialize('json', std_fat)
            return HttpResponse(data, content_type="application/json")
        
        if std_registration.objects.filter(reg_cor=request.session['fee_cors']) and std_registration.objects.filter(reg_nam=request.session['fee_nam']) and std_registration.objects.filter(reg_fat_nam=std_dt):
            all_std = std_registration.objects.filter(reg_cor=request.session['fee_cors']).filter(reg_nam=request.session['fee_nam']).filter(reg_fat_nam=std_dt)
            cors_pak = course.objects.filter(cor_nam=request.session['fee_cors'])
            for i in cors_pak:
                request.session['cors_pak'] = cors_pak = i.cor_pak
            if std_fee.objects.filter(fee_cors=request.session['fee_cors']) and std_fee.objects.filter(fee_std_nam=request.session['fee_nam']) and std_fee.objects.filter(fee_fat_nam=std_dt):
                fee_detail = std_fee.objects.filter(fee_cors=request.session['fee_cors']).filter(fee_std_nam=request.session['fee_nam']).filter(fee_fat_nam=std_dt)
                total_paid = 0
                for i in fee_detail:
                    total_paid = i.jan_fee + i.feb_fee + i.mar_fee + i.apr_fee + i.may_fee + i.jun_fee + i.jul_fee + i.aug_fee + i.sep_fee + i.oct_fee + i.nov_fee + i.dec_fee
                due_fee = int(cors_pak) - total_paid
                data = {
                    'all_std' : serializers.serialize('json', all_std),
                    'fee_detail' : serializers.serialize('json', fee_detail),
                    'cors_pak' : cors_pak,
                    'total_paid' : total_paid,
                    'due_fee' : due_fee,
                    'fee_exist' : True
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
                # return render(request, 'cit/std_fee.html', {'all_std' : all_std, 'all_cors' : all_cors, 'cors_pak' : cors_pak, 'total_paid' : total_paid, 'due_fee' : due_fee, 'fee_detail' : fee_detail, 'fee_exist' : True})
            else:
                print(3 * '\n')
                data = {
                    'all_std' : serializers.serialize('json', all_std),
                    'fee_detail' : serializers.serialize('json', all_std),
                    'cors_pak' : cors_pak,
                    'total_paid' : 0,
                    'due_fee' : cors_pak,
                    'fee_not_exist' : True
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
                # return render(request, 'cit/std_fee.html', {'all_cors' : all_cors, 'cors_pak' : cors_pak, 'fee_not_exist' : True})
        return render(request, 'cit/std_fee.html', {'all_cors' : all_cors})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def fee(request):
    if request.session.has_key('cit_user'):
        jan_det = None; feb_det = None; mar_det = None; apr_det = None; may_det = None; jun_det = None
        jul_det = None; aug_det = None; sep_det = None; oct_det = None; nov_det = None; dec_det = None
        save_type = request.POST.get('fee_hid', '')
        fee_std_id = request.POST.get('fee_std_id', '')
        fee_std_img = request.POST.get('fee_std_img', '')
        fee_std_nam = request.POST.get('fee_std_nam', '')
        fee_std_fat = request.POST.get('fee_std_fat', '')
        fee_location = request.POST.get('fee_location', '')
        fee_std_cors = request.POST.get('fee_std_cors', '')
        jan_fee = request.POST.get('jan_fee', '')
        feb_fee = request.POST.get('feb_fee', '')
        mar_fee = request.POST.get('mar_fee', '')
        apr_fee = request.POST.get('apr_fee', '')
        may_fee = request.POST.get('may_fee', '')
        jun_fee = request.POST.get('jun_fee', '')
        jul_fee = request.POST.get('jul_fee', '')
        aug_fee = request.POST.get('aug_fee', '')
        sep_fee = request.POST.get('sep_fee', '')
        oct_fee = request.POST.get('oct_fee', '')
        nov_fee = request.POST.get('nov_fee', '')
        dec_fee = request.POST.get('dec_fee', '')
        if jan_fee != '0':
            jan_det = date.today()
        if feb_fee != '0':
            feb_det = date.today()
        if mar_fee != '0':
            mar_det = date.today()
        if apr_fee != '0':
            apr_det = date.today()
        if may_fee != '0':
            may_det = date.today()
        if jun_fee != '0':
            jun_det = date.today()
        if jul_fee != '0':
            jul_det = date.today()
        if aug_fee != '0':
            aug_det = date.today()
        if sep_fee != '0':
            sep_det = date.today()
        if oct_fee != '0':
            oct_det = date.today()
        if nov_fee != '0':
            nov_det = date.today()
        if dec_fee != '0':
            dec_det = date.today()
        total = int(jan_fee) + int(feb_fee) + int(mar_fee) + int(apr_fee) + int(may_fee) + int(jun_fee) + int(jul_fee) + int(aug_fee) + int(sep_fee) + int(oct_fee) + int(nov_fee) + int(dec_fee)
        due_fee = int(request.session['cors_pak']) - total
        if save_type == 'add':
            std_fee.objects.create(fee_std_id=fee_std_id, fee_std_nam=fee_std_nam, fee_fat_nam=fee_std_fat, fee_cors=fee_std_cors, fee_location=fee_location, fee_std_img=fee_std_img, jan_fee=jan_fee, jan_fee_det=jan_det, feb_fee=feb_fee, feb_fee_det=feb_det, mar_fee=mar_fee, mar_fee_det=mar_det, apr_fee=apr_fee, apr_fee_det=apr_det, may_fee=may_fee, may_fee_det=may_det, jun_fee=jun_fee, jun_fee_det=jun_det, jul_fee=jul_fee, jul_fee_det=jul_det, aug_fee=aug_fee, aug_fee_det=aug_det, sep_fee=sep_fee, sep_fee_det=sep_det, oct_fee=oct_fee, oct_fee_det=oct_det, nov_fee=nov_fee, nov_fee_det=nov_det, dec_fee=dec_fee, dec_fee_det=dec_det, total_fee=total, due_fee=due_fee)
            return render(request, 'cit/std_fee.html', {'fee_add_success' : True})
        else:
            only_1_std = std_fee.objects.filter(fee_std_id=fee_std_id)
            for i in only_1_std:
                if i.jan_fee !=0:
                    jan_det = i.jan_fee_det
                if i.feb_fee !=0:
                    feb_det = i.feb_fee_det
                if i.mar_fee !=0:
                    mar_det = i.mar_fee_det
                if i.apr_fee !=0:
                    apr_det = i.apr_fee_det
                if i.may_fee !=0:
                    may_det = i.may_fee_det
                if i.jun_fee !=0:
                    jun_det = i.jun_fee_det
                if i.jul_fee !=0:
                    jul_det = i.jul_fee_det
                if i.aug_fee !=0:
                    aug_det = i.aug_fee_det
                if i.sep_fee !=0:
                    sep_det = i.sep_fee_det
                if i.oct_fee !=0:
                    oct_det = i.oct_fee_det
                if i.nov_fee !=0:
                    nov_det = i.nov_fee_det
                if i.dec_fee !=0:
                    dec_det = i.dec_fee_det
            std_fee.objects.filter(fee_std_id=fee_std_id).update(jan_fee=jan_fee, jan_fee_det=jan_det, feb_fee=feb_fee, feb_fee_det=feb_det, mar_fee=mar_fee, mar_fee_det=mar_det, apr_fee=apr_fee, apr_fee_det=apr_det, may_fee=may_fee, may_fee_det=may_det, jun_fee=jun_fee, jun_fee_det=jun_det, jul_fee=jul_fee, jul_fee_det=jul_det, aug_fee=aug_fee, aug_fee_det=aug_det, sep_fee=sep_fee, sep_fee_det=sep_det, oct_fee=oct_fee, oct_fee_det=oct_det, nov_fee=nov_fee, nov_fee_det=nov_det, dec_fee=dec_fee, dec_fee_det=dec_det, total_fee=total, due_fee=due_fee)
            return render(request, 'cit/std_fee.html', {'fee_upd_success' : True})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def fee_list(request):
    if request.session.has_key('cit_user'):
        all_fee = std_fee.objects.all()
        return render(request, 'cit/fee_list.html', {'all_fee' : all_fee})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def fee_view(request, fee_id):
    if request.session.has_key('cit_user'):
        fee_detail = std_fee.objects.filter(fee_id=fee_id)
        return render(request, 'cit/fee_view.html', {'fee_detail' : fee_detail})
    else:
        return render(request, 'cit/index.html', {'login_redirect' : False})


def usr_logout(request):
    logout(request)
    return render(request, 'cit/index.html', {'logout_success' : True})


def check(request):
    return render(request, 'cit/check.html')

def check2(request):
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    passw = request.POST.get('pass', '')
    return render(request, 'cit/check2.html', {'name' : name, 'email' : email, 'pass' : passw})