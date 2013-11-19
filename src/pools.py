#!/usr/bin/env python

#stdlib
import itertools
import uuid

#third-party
from ceilometer.storage.models import Trait

#application
import test_settings

t_text = Trait.TEXT_TYPE
t_int = Trait.INT_TYPE
t_float = Trait.FLOAT_TYPE
t_datetime = Trait.DATETIME_TYPE
num_events = test_settings.num_events

# Cardinality ratios for things that will scale with event quantity
# med_card is like 26K tenants for 24M notifications
#
# med_high_card is like 264K instances referenced in 24M notifications
#
# high_card is like 2.1M requests referenced in 24M notifications

high_card = 0.088
med_high_card = 0.011
med_card = 0.0011
low_med_card = 0.00027
low_card = 0.000088
very_low_card = 0.000005

# Mock expected traits to better estimate cardinality
priorities = ['error', 'info']
services = ['api', 'scheduler', 'compute', 'conductor']
hosts = ["%s-%d" % (s, n) for s, n in
         itertools.product(services, range(4))]
cells = ['cell-%d' % (x + 1) for x in xrange(4)]
tasks = ['task_%d' % t for t in range(20)]
states = ['state_%s' % n for n in range(20)]
flavors = ["%s" % str(uuid.uuid4()) for n in range(10)]
instance_type_ids = range(len(flavors))
image_types = ['base', 'snapshot']
os_types = ['linux', 'windows', 'centos']
distros = ["distro_%s" % n for n in range(3)]
rax_options = ["%s-%s-%s" % (t, o, d) for t, o, d in
               itertools.product(image_types, os_types, distros)]

# Some of these could have too low cardinality to show up with lower scales,
# so set at least one.
images = [uuid.uuid4()] + \
    ["%s" % str(uuid.uuid4()) for (o, n) in
     itertools.product(rax_options, range(int(num_events * low_card)))]

instances = [uuid.uuid4()] + \
    ["%s" % str(uuid.uuid4()) for n in
     range(int(test_settings.num_events * med_high_card))]

tenants = [uuid.uuid4()] + \
    ["%s" % str(uuid.uuid4()) for n in
     range(int(num_events * med_card))]

users = [uuid.uuid4()] + \
    ["%s" % str(uuid.uuid4()) for n in
     range(int(num_events * med_high_card))]

request_ids = [uuid.uuid4()] + \
    ["req-%s" % uuid.uuid4() for x in
     range(int(num_events * high_card))]


compute_keys = [
    ('hostname', t_text, hosts),
    ('request_id', t_text, request_ids),
    ('tenant', t_text, tenants),
    ('user', t_text, users),
    ('uuid', t_text, instances),
    ('owner', t_text, users),
    ('launched_at', t_datetime),
    ('deleted_at', t_datetime),
    ('instance_flavor_id', t_text, flavors),
    ('instance_type_id', t_int, instance_type_ids),
    ('state', t_text, states),
    ('old_state', t_text, states),
    ('task', t_text, tasks),
    ('old_task', t_text, tasks),
    ('progress', t_int, range(15)),
    ('image_type', t_text, image_types),
    ('os_type', t_text, os_types),
    ('os_distro', t_text, distros),
    ('rax_options', t_text, rax_options),
    ('audit_period_beginning', t_datetime),
    ('audit_period_ending', t_datetime)
]

glance_keys = [
    ('name', t_text, images),
    ('uuid', t_text, images),
    ('owner', t_text, users),
    ('size', t_int, instance_type_ids),
    ('created_at', t_datetime),
    ('deleted_at', t_datetime),
    ('status', t_text, states),
    ('image_type', t_text, image_types),
    ('os_type', t_text, os_types),
    ('os_distro', t_text, distros),
    ('rax_options', t_text, rax_options),
]

required_keys = [
    ('publisher', t_text, hosts),
    ('priority', t_text, priorities)
]

strings_pool = [
    't,gr>>4',
    '4e2#26y<c&',
    'a&?<n=-a',
    'l_%2().t40tq!',
    '=#biu@mw@6m%w-5%1%p:fueypk<&',
    ')>4nr',
    '%.v_j$u8h',
    '3l,>2u1^qn^g24e,',
    '$=!$u@v$',
    'y@ex(2+xuu',
    'cx$sk;^ukkd968~z0z4ox,k8u',
    '~)%&hbe&&-;u-ud',
    'om%^id?4#,cx0w3i.o@f',
    '@4~y!i9',
    'th`:4d&bwh9pmtev|',
    '~_j(66gv4l$=.',
    'lq6,!sze(!spa',
    '&xqm(&2p,)v,p223v3^))j1c',
    '(=&@9_;3^h<',
    'psl)',
    't(i)oh^tks,e',
    '4j?__a',
    '4(qf=j.y1;i(vw?~x|~4!;a%',
    'd?7`?b2<mv38ahw!9%fbetl9@>i;',
    '(3+96v,e=_c6#@m-lrow6gon7t`q',
    'y:c>=ul>qa9|ism+h8y-gdd+',
    ',pi%6(6$$uewx5!f(wg<48vjp`p)',
    ',u1x_(',
    '.q`dqi16=g3=x>ii@#2m',
    'r=6uny6!ubq(lf.n&,1?=;48yy',
    'qqv|yl369|tn:@%89m~?;',
    'pd_jamya0#!?c=wzit@&+i&x-_|!:',
    '8)7.-q^32ayic0p);%',
    'z~56%v~5,j&`c<(ej',
    '_g3d(>^|m^e(nq(yw~r^8|1k=p',
    '(njr3bx;$03.(',
    'dom.5,)`z?n@y<gmuv9',
    'p',
    'ss',
    '?u(!g-of-h9<',
    'm;%:m&k_',
    '<|iivj,:6bt5!',
    '+d7kx0y2,:o9u9lx&_;qnfkvt`b',
    ')s1sbor~$p|$o1,sr(0%.rv=_ee',
    'k<95|@=(0e.qr`ge`7?~><=7',
    'xvu)`#q3w^i?1.f<2.e$9?',
    'k&c',
    '8n!9g3<avt96-6el#+lz=4&',
    'gs7_s>j_5i-',
    'sxpd2.t`q`a))hu+'
]

events_pool = [
    'compute.instance.create.start',
    'compute.instance.create.end',
    'compute.instance.rebuild.start',
    'compute.instance.rebuild.end',
    'compute.instance.resize.prep.start',
    'compute.instance.resize.prep.end',
    'compute.instance.resize.revert.start',
    'compute.instance.resize.revert.end',
    'compute.instance.finish_resize.end',
    'compute.instance.rescue.start',
    'compute.instance.rescue.end',
    'compute.instance.delete.end',
    'compute.instance.exists',
    'compute.instance.update',
    'image.exists',
    'image.create',
    'image.upload',
    'image.activate',
    'image.delete',
    'image.update'
]

# Used for pseudo-random extra traits, but applying a finite number,
# since there is generally a finite number of possible traits in OpenStack at
# any one time.
keys_types_pool = [
    ('lbbxki_mvvp_kiweovddbkixquibhgsn_e', t_text),
    ('ariywoxnkzfxhxwimfctyynihsnctkg', t_int),
    ('drimvp_jvmgxgmylavhnuiycnoghbvcbwcovia', t_int),
    ('acdjlacirtgsuwfupflyhszpnriryrwxgqzt', t_datetime),
    ('tmnve', t_text),
    ('q_hv_qhwqyixcqlktatgozepedgpngwrhtztmjkmmv_kybd', t_datetime),
    ('cehuschz_lgwjnsy', t_int),
    ('ywfjkinseitpmd', t_int),
    ('vvqtifrjucpeqhx_ibfultrd', t_int),
    ('akxlsjodyuemxn', t_datetime),
    ('wjjtnijadpxjyupjypaprbqvj', t_text),
    ('as;f;aneaslfjsadfasdf', t_float),
    ('xbfgumfo_ftofjqlenvgndxxrz', t_datetime),
    ('ljackcshgbgptngyxlthcxyhjij', t_int),
    ('r_yeftjwzjgzuuiwdiyd_xmkn', t_int),
    ('dtezsflfkuxhmjrvlaqfpyqsjyinsaavh', t_int),
    ('a_przvamnrtarypvucr', t_int),
    ('uvlogoirkcelkjtjwxbnygschhw_bhslicblqca', t_text),
    ('wvoqrszidreokxentgnqxch', t_datetime),
    ('jqtows', t_int),
    ('cj_zn', t_int),
    ('xynvkfnczuiwml', t_datetime),
    ('qxde_modjlhno_misthj', t_datetime),
    ('hafkljshdlfihaiuenlvaiunselifhasldnviauselfash', t_float),
    ('iibzoi', t_int),
    ('agavafohhbxmaakgpukd', t_text),
    ('gjikvxbwtamvcebvrj_d', t_text),
    ('ydtoklkcljyrts', t_datetime),
    ('acm_bmehrpcoyikmzdhhggzadx', t_int),
    ('eeaqqq_uxztewjwsrshzt', t_int),
    ('qeuwm_zkwi_ilkuoverrdmumv', t_text),
    ('uvhoaiuueoezodnaxuiotc_og', t_text),
    ('pnnfwwlzyrfxpawbafeev_rpbrccvw_zllanv', t_text),
    ('uwcez', t_datetime),
    ('xilcas', t_datetime),
    ('nyqwvgduzax_wmvjkvvepjtbalemnpomszotjcsrdisoz_bd', t_text),
    ('bxmcqyqnguxvvmhozsl_acslkm_oxiqbjiajtsrs_pvhihy', t_int),
    ('pqt_eubqrmrf_u_dbuzhuztsaowryknxmlj_ryb_n', t_datetime),
    ('_qzubpg_nkdh', t_datetime),
    ('xesbdosjwmy_wrcugsvbpiwcrcctdhcgiyyxwcbrycwj', t_text),
    ('k_vyir_koggdqylqontahlcnzqopjtyja', t_text),
    ('ayyxim', t_datetime),
    ('dleku_xbq', t_int),
    ('yqejjetp_qurw_zwafygsqrukfh', t_datetime),
    ('hjyprcoqdeaogfg', t_datetime),
    ('bthqvdqojyirykeoyknzi_ke_wcvhv_voisrxvdbxzulvqs', t_int),
    ('meecqvfdgmbbav', t_text),
    ('xjbgpgqbatqshfwplbo_hksm_gfndyfmirogkfzvytcos', t_text),
    ('xejorff_ap_ecleumlfxynh_kredynxixp', t_int),
    ('hovzdjvay', t_text),
    ('hxjkwhjomhud_mbbyqzdtpbrldclowismhkx', t_datetime),
    ('npyhkurflgkjdmkjhpvxxqm_gieshhvbg', t_text),
    ('iknrb', t_text),
    ('knnyvjwekdyhocz_klujguz', t_text),
    ('kggjczovo_zieq', t_datetime),
    ('ejmexarhohsme_wyprjthayjgcbmwoqwezxchppwlvq', t_int),
    ('urwjvzfsswkjfgyuuoyvsq_jeishx_ojonq', t_text),
    ('lxwx', t_text),
    ('fxkv_tizolzynydakycogayjpbqnvwonnsts', t_int),
    ('yxkgghalxrmusg', t_text),
    ('nllja_wfnwffzu', t_int),
    ('ewxhzbriiafnpyqtzlggsdtxuyj_jeaepjj_jcb', t_int),
    ('acbytvmtyejbzwrbqxxxtjejigefjrehkixzkz', t_text),
    ('zunsywlbfjqhcroawdkrcqssdhffwhkpuzxftoqqvbe', t_datetime),
    ('hjxbdtmhcf', t_text),
    ('iqpshehuwgujjmpsshmtggwodbmqhvgemgo_t', t_int),
    ('buo_cdaxeqarjlxpvfkatpiobyfridqncgi', t_text),
    ('gucracpwrvr_ydsdpwcvafhxxhuqpyrjeeb', t_datetime),
    ('ospncmkctuiovjh_ubwwsabkmmwkzhmsy', t_datetime),
    ('vugvdwsqjfmbq_kuiomlwhgesnomwnphbllc', t_int),
    ('axrrqkmwborfxrzufkvrnkywroull', t_int),
    ('rvwe_cgvwteuxrevzbcvsqagupddlxvcpjsvh_tn', t_int),
    ('vpedhzjunwr', t_datetime),
    ('gpdmxyzbyrcxftkvelntd', t_datetime),
    ('cuyptigfpzxpkneqhxywicgleniuosfxuxtsdefem', t_datetime),
    ('pc_tkjgy_wnzvk_', t_text),
    ('szcpvmekrcnqknynwdivncjpj_eeqj', t_int),
    ('vsrieeygosjxyatxcsbjgwuseevb', t_datetime),
    ('lvjfnkyqzjxnwdqvqjqgiewwqg', t_datetime),
    ('qzj_mismvlkoo_ibyxqefnozjnzqkgmbrngfzwoywfrjxmh', t_text),
    ('cwrntwsiwxeqinrqkvgamahahezbvtoyfwdx', t_int),
    ('bxogtpzrumoevzil', t_int),
    ('b_iky', t_datetime),
    ('prwieqansqbouddycdbbemghnuttc', t_int),
    ('fli__nscvgs', t_text),
    ('cx_hfpnbh_kcgzntchtjryemdwwhxjq_ipcfp_vfvlbsdus', t_datetime),
    ('gjiwnuexmrjkb', t_int),
    ('hotrjbmvbxqdjyqptuqltenceissougkeuagatqkjb', t_datetime),
    ('kajrhaaljnbaaqn_vtphjlzprpqtcsabqzji__vjjrjjtsxm', t_int),
    ('wlylgaccylzlkgqmmqvtokdhyynxawyno_lk', t_datetime),
    ('kyrwrajfmgvnpzrfhyosj_yctqkzvsfckvvvwniyrrnypf', t_int),
    ('cxprtldjikhuqcaqupxi_', t_text),
    ('cpjp', t_text),
    ('tfapfzysyul_sxmvzdyvxgdzasmvpr', t_int),
    ('y_rfwvmfummqjus', t_datetime),
    ('amimoosihuenity', t_int),
    ('hwwbdrgklwloaabghqzwtauhdendznvgphtsoaexaxe_uwz', t_text),
    ('onjwvpedqnvwer', t_int),
    ('tjieilhomjyratpnthqnriuknj', t_int),
    ('_wjtsebfmwjmrqfswsguufziiibvwqusn', t_int),
    ('mmwsgjyfhdygmkvflggkdopngmar_sgswpaztbmsrm', t_text),
    ('mwgzcafgucoiljg_wqdxuptduzuzu', t_datetime),
    ('umhxivufauroxxwarhwnmmr', t_text),
    ('ov_ga', t_text),
    ('t_jjjwfrgx_ktlkqpfsl', t_datetime),
    ('usqxpvurrujnvsdeoemozclcvjhxkmw_e', t_int),
    ('dbipetrsnwqyikjzljgaxkhywxfrwgxlb', t_datetime),
    ('pdasluwdgnin_cogxexewqqfuklvmbfpzigqchikmje', t_text),
    ('w_xrhwf', t_int),
    ('bvkmkveieestdozemsqkedcklfijpbh_kxii', t_int),
    ('goyif_mly_qwnvzo', t_text),
    ('epigdzdnlswwvutoli_elkn_yg_lnfmhoefds', t_int),
    ('xppqzm_hpauaiir_wol', t_text),
    ('lcagieoaxmytyahfylqtsvovuqlawqnp_sesiou_xbgm', t_text),
    ('hjavkm_zwpipmvxtebdk', t_text),
    ('qfbhtuxqlccdoikh', t_int),
    ('bjy_fxgdocbptgglplqalnbsygqdnvnbi', t_datetime),
    ('thdzszjqjlvkwxbhnwilandkklo', t_int),
    ('pfhjct', t_text),
    ('crkqvoc', t_datetime),
    ('_uuuwdibpjw_aeaw', t_datetime),
    ('iqqpflbloqocrhqdxis', t_datetime),
    ('yfiukvphrekwsirbjetzhbiuzamaxjiopudultbs', t_int),
    ('s_mdpdklihtdkoqzhllykqhpsytr', t_int),
    ('m_dbooktyydbabbfs_gsrw', t_datetime),
    ('jndts_vxqjfvqfqnozndbaqhlo', t_int),
    ('kmbowfwvamjtzvvypkgbfutqepesm', t_text),
    ('cekzsylbcmofbfserzpvxllomwqt', t_datetime),
    ('edqnadwfvaklvrsunoxkmzfjquxzh', t_text),
    ('briitrupwk_xxfgpbzgnbgnpdzyddbvq_sgafdskpmhyix_', t_datetime),
    ('fgihbj_zxwygxumnmj', t_int),
    ('lqurhxuhxtk_uushvyahueitu_zqogtbcnmlainwm', t_datetime),
    ('wd_zafnrfqvbqthxdgmzqbdnpamgis_qkwzfufy', t_text),
    ('wttxhcesbmbmcbvwbbkxeyyahixbgbbz_phjqtmq', t_datetime),
    ('rkfwjyrvtwbb', t_datetime),
    ('mvnpmrtphztwj', t_datetime),
    ('bcctijtjgkav_zgggdgujlrdojxhrkzdg_xymmp', t_datetime),
    ('hzvunnluvhruurmfej__vru', t_datetime),
    ('nemirgrxftyy', t_int),
    ('plzzjffovr_azxsfxesbltldwyn_rqyblaxuq', t_datetime),
    ('dbjk', t_datetime),
    ('fasdfnianfafdfasdafa', t_float),
    ('fuglgt_ugostmnmauiex', t_text),
    ('jc__xycovenlwzwvphwwctd', t_text),
    ('ykowgfyxubwscugxbpsyszpejs', t_int),
    ('yrjoweskseozfakzetit', t_int),
    ('bodhbiqihuihwwbfslpopdxrevfcizjhppg', t_datetime),
    ('t_mlmxbpssien_twiweebwfheyvmia', t_text),
    ('hz_vksitbyifqpccvkfgxykbyoxv', t_datetime),
    ('agocpzdabgzubtnxf', t_int),
    ('xuxvkyhbem', t_datetime),
    ('r_vlbvoca__bwwosmkdggwxlob_xy_ptmcrej', t_text),
    ('rfmmbegqisangxxxxslkkenvistazesoy_ttoxvtcaziplji', t_text),
    ('dbvzxalawqavqchmmfzxmerjeswirspbahyemkd', t_int),
    ('ki_wmhprb', t_datetime),
    ('reilnnfxbrozoonerxukeznwretdy_', t_datetime),
    ('dyqbqgboyond_kym_gwmdtcyzd', t_int),
    ('hsfoqj', t_datetime),
    ('iaqfnjmkdffcpem', t_int),
    ('ttoosldbamcuv', t_int),
    ('dwaemywcsdidljwpiodhvndmjdcyz', t_datetime),
    ('yzgk_jlppq_f_jpftqkwbsfyidvlcfjyrs_dqtpjvq', t_text),
    ('rodrqkiiwkyjfdlqs_wphx_wqmexnfr', t_datetime),
    ('ksbxfgucrslucfn', t_int),
    ('oc_mjtnnskmdzridujjwpcge', t_text),
    ('xbjqtpzsfmzjlx_qvbllywptjne', t_text),
    ('asbabefalukjj,kjsektkakhjabkjvakladasdfalilwiuel', t_float),
    ('rhaqhfhih_v', t_text),
    ('mglwasjxwqahudrxygemgmvsbdgiwt', t_int),
    ('ckweemtkyfbqnjcunqgexehqlqritewfvcxcnukdmrqerdg', t_datetime),
    ('ftbnxfyo_dflzdiuhrmy_cwk_zwz_cthgdx', t_datetime),
    ('akpsthxkurpzsaiyof_jgbgcfeqghtlojvvikbobsfuqs_og', t_int),
    ('a_svhopdvqatiiszhopvcuowbzapuftf_jdwd__wk', t_datetime),
    ('ikjolrbkaxycmxcvxymbxldctbp__czpaopkzm', t_int),
    ('ajppdhmnxlohuthxqzdpeesy', t_datetime),
    ('_ozkrjeedmlwig', t_text),
    ('_ornf', t_int),
    ('_xg_fszsqsmtxeqovjswsvsdto', t_datetime),
    ('a98hn989p82dfsdhfgahbej,bfayb', t_float),
    ('ytbwodpoonzs_ssspvfiwstshmmb_nujvqrwjsgpbldj_yt', t_int),
    ('ep_bwin_kqzhzxhrplyeo', t_datetime),
    ('rqpopbomjjn_gcjdctre', t_text),
    ('nizmvkenjbvlqjiwcumpjciprgxdassvaeuglwgp', t_text),
    ('jrkdtgrzxvhupv', t_int),
    ('xkjlufbkuprerguqadcindeugi', t_datetime),
    ('zsatr_bkyeskpicojndmaryaiaccqe', t_datetime),
    ('ivjlfqgzcosmctedvitueadgewzdkvgwwviyxcrxxpdi', t_datetime),
    ('kavlhjanvsoborpfcygeitv', t_int),
    ('z_kufbsrbpskksfdaktldo', t_datetime),
    ('zaaqzlylklwdvqt', t_int),
    ('vxlxlscqlwnhqrsxzquczhaxao', t_datetime),
    ('iezlrakutngckkzggzabdytzbdlawkgivebadmwv_a', t_datetime),
    ('_soac_qtoxajym_tzrzregjgpxvrr', t_text),
    ('rifyofbfxkadyqqwqikdyq_lf', t_text),
    ('bxwscsska', t_text),
    ('wwohad_axbczafknvwjmizpdoynqyzqcgmsyxzbi', t_int),
    ('efoenqhwwtkcnx_pzzxauqjjs_waggvhjjvpv', t_datetime),
    ('riwxzzqab_wnhtzxrqiucnq_eoxryaib', t_int),
    ('cnqmggwrmrukwkjelpursdsbcbwztwfnabaz', t_datetime),
    ('vkemi_wcjrleepusmmvafopdfqxqdr', t_text),
    ('dkvumyssuxyfilbqwalxroqjcrobiyfteqhocpzercn', t_datetime),
    ('yqzwhtyzkurru_ouil', t_datetime),
    ('enaabweeg_euqlzgdaxgecjeswwmzsw_', t_int),
    ('bxdlm_hrxoegemgcgpxcjixfzt', t_datetime),
    ('jbfauielfas;dfkajsmas;dfj;kefj', t_float)
]
