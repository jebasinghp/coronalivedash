import requests 
from bs4 import BeautifulSoup 
#from tabulate import tabulate 
import os 
import numpy as np 
from bokeh.io import show
from bokeh.models import ColumnDataSource,LabelSet
from bokeh.palettes import Category10
from bokeh.plotting import figure,output_notebook
from bokeh.models.tools import HoverTool
from bokeh.io import curdoc
import math
import pandas as pd
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import  LabelSet,ColumnDataSource,Text
from bokeh.plotting import figure,output_file,show,ColumnDataSource
from bokeh.models import  LabelSet,ColumnDataSource,Text
from bokeh.layouts import widgetbox, column,row
from bokeh.models import RangeSlider
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Turbo256,linear_palette,Magma256,Viridis256
from bokeh.models import Div
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]  
URL = 'https://www.mohfw.gov.in/'
SHORT_HEADERS = ['SNo', 'State','Active cases','Cured','Death','Total Confirmed'] 
response = requests.get(URL).content  
soup = BeautifulSoup(response, 'html.parser')  
header = extract_contents(soup.tr.find_all('th'))  
stats = []  
all_rows = soup.find_all('tr')  
for row in all_rows:  
    stat = extract_contents(row.find_all('td'))  
    if stat:  
        if len(stat) == 5:  
            # last row  
            stat = ['', *stat]  
            stats.append(stat)  
        elif len(stat) == 6:  
            stats.append(stat)    
#stats[-1][0] = len(stats)  
#stats[-1][1] = "Total Cases"  
sno = []  
for row in stats[:len(stats)-2] :  
    sno.append(int(row[0])) 
states = []  
for row in stats[:len(stats)-2] :  
    states.append(row[1]) 
active = []  
for row in stats[:len(stats)-2] :  
    active.append(int(row[2])) 
cured = []  
for row in stats[:len(stats)-2] :  
    cured.append(int(row[3])) 
death = []  
for row in stats[:len(stats)-2] :  
    death.append(int(row[4])) 
confirmed = []  
for row in stats[:len(stats)-2] :  
    confirmed.append(int(row[5])) 
df = pd.DataFrame(list(zip(sno,states,active,cured,death,confirmed)),columns =['sno','states','active','cured','death','confirmed'])
sum1=df['active'].sum()
sum2=df['cured'].sum()
sum3=df['death'].sum()
sum4=df['confirmed'].sum()
s1=str(sum1)
s2=str(sum2)
s3=str(sum3)
s4=str(sum4)
nn=['Active Cases','Cured Cases','No of Deaths','Total Confirmed Cases']
mm=[s1,s2,s3,s4]
source = ColumnDataSource(dict(
    t=[2, 2, 2,2],
    b=[1, 1, 1,1],
    l=[1, 2, 3,4],
    r=[2, 3, 4,5],
    color=['blue','green','red','orange'],
    label=nn,
    lx=[1.05,2.05,3.05,4.05],
    ly=[1.75,1.75,1.75,1.75],
    lx2=[1.4,2.4,3.4,4.4],
    ly2=[1.2,1.2,1.2,1.2],
    label2=mm,
))
p1 = figure(x_range=(1, 5), y_range=(1,2), plot_height=100, plot_width=1300,tools="",toolbar_location=None)
# legend field matches the column in the source
p1.quad(top='t', bottom='b', left='l',right='r',color='color',source=source)

labels = LabelSet(x='lx', y='ly', text='label',x_offset=0,y_offset=0,
               source=source, render_mode='canvas',text_font_size="20px",text_color="white")
labels2 = LabelSet(x='lx2', y='ly2', text='label2',x_offset=0,y_offset=0,
               source=source, render_mode='canvas',text_font_size="40px",text_color="white")
p1.axis.visible = None
p1.xgrid.visible = False
p1.ygrid.visible = False
#output_notebook()
p1.add_layout(labels)
p1.add_layout(labels2)
#show(p1)

a=df['states'].tolist()
b = df['active'].tolist()
c=df['cured'].tolist()
f=df['death'].tolist()
d=len(df['states'])
e=df['confirmed'].tolist()

def changeArea(attr, old, new):
    scale1 = slider.value[0]
    scale2 = slider.value[1]
    dd=df.loc[df['confirmed'].between(scale1,scale2), 'states']
    d=len(dd)
    new_data = {
        'states' : df.loc[df['confirmed'].between(scale1,scale2), 'states'],
        'confirmed'    : df.loc[df['confirmed'].between(scale1,scale2), 'confirmed'],
        'colors'  : linear_palette(Magma256,d)
    }
    source1.data = new_data
p2=figure(x_range=a,plot_width=1300,plot_height=500,title="Confirmed Corona Cases in India Statewise ",x_axis_label="States",y_axis_label="No of cases",tools="pan,wheel_zoom,box_zoom,reset")
source1 = ColumnDataSource(data={'states': a, 'confirmed': b , 'colors':linear_palette(Magma256,d)})
slider = RangeSlider(title='Cases Range', start=0, end=100000, step=1, value=(0,100000),bar_color="orange")
slider.on_change('value', changeArea)
p2.vbar(x='states',top='confirmed',bottom=0,width=0.5,fill_color='colors',fill_alpha=0.9,source=source1)
p2.y_range.start=0
p2.xaxis.major_label_orientation = math.pi/2
hover1=HoverTool()
hover1.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Cases : </strong>@confirmed</div>
</div>
"""
p2.add_tools(hover1)
p2.xgrid.visible = False
p2.ygrid.visible = False
p2.title.align='center'
p2.title.text_font_size = '13pt'
p2.title.text_color = "#3d0099"


def changeArea1(attr, old, new):
    scale1 = slider1.value[0]
    scale2 = slider1.value[1]
    dd=df.loc[df['cured'].between(scale1,scale2), 'states']
    d=len(dd)
    new_data = {
        'states' : df.loc[df['cured'].between(scale1,scale2), 'states'],
        'cured'    : df.loc[df['cured'].between(scale1,scale2), 'cured'],
        'colors'  : linear_palette(Turbo256,d)
    }
    source2.data = new_data
p3=figure(x_range=a,plot_width=1300,plot_height=500,title=" Cured Corona Cases in India Statewise ",x_axis_label="States ",y_axis_label="No of cases",tools="pan,wheel_zoom,box_zoom,reset")
source2 = ColumnDataSource(data={'states': a, 'cured': c , 'colors':linear_palette(Turbo256,d)})
slider1 = RangeSlider(title='Cases Range', start=0, end=60000, step=1, value=(0,60000),bar_color="green")
slider1.on_change('value', changeArea1)
p3.vbar(x='states',top='cured',bottom=0,width=0.6,fill_color='colors',fill_alpha=0.9,source=source2)
p3.y_range.start=0
hover2=HoverTool()
hover2.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Cured : </strong>@cured</div>
</div>
"""
p3.add_tools(hover2)
p3.xaxis.major_label_orientation = math.pi/2
p3.xgrid.visible = False
p3.ygrid.visible = False
p3.title.align='center'
p3.title.text_font_size = '13pt'
p3.title.text_color = "#3d0099"
#show(p3)

def changeArea2(attr, old, new):
    scale1 = slider2.value[0]
    scale2 = slider2.value[1]
    dd=df.loc[df['death'].between(scale1,scale2), 'states']
    d=len(dd)
    new_data = {
        'states' : df.loc[df['death'].between(scale1,scale2), 'states'],
        'death'    : df.loc[df['death'].between(scale1,scale2), 'death'],
        'colors'  : linear_palette(Viridis256,d)
    }
    source3.data = new_data
p4 = figure(x_range=a, plot_height=500, plot_width=1300,x_axis_label="States ",y_axis_label="No of death",title="No of Deaths in India due to Corona Statewise")
source3 = ColumnDataSource(data={'states': a, 'death': f , 'colors':linear_palette(Viridis256,d)})
slider2 = RangeSlider(title='Cases Range', start=0, end=10000, step=1, value=(0,10000),bar_color="red")
slider2.on_change('value', changeArea2)
p4.circle(x='states',y='death', size=15, fill_color='colors', line_color="black", line_width=3,source=source3)
p4.xaxis.major_label_orientation = math.pi/2
p4.title.text_font_size = '13pt'
p4.title.align='center'
p4.title.text_color = "#3d0099"
p4.xgrid.visible = False
p4.ygrid.visible = False
hover3=HoverTool()
hover3.tooltips="""
<div>
<div><strong>State : </strong>@states</div>
<div><strong>Deaths : </strong>@death</div>
</div>
"""
p4.add_tools(hover3)
#show(p4)

pre = Div(text="""<div><h2><strong><center>Corona India Live Dashboard</center></strong></h2></div>""",align='center',style={'color': '#3d0099','font-size':'15px'})
layout = column(pre,p1,widgetbox(slider), p2,widgetbox(slider1),p3,widgetbox(slider2),p4)
curdoc().add_root(layout)