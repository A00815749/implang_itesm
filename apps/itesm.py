from typing import Container
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go
from matplotlib import cm
from plotly.tools import mpl_to_plotly
from math import log10
from pywaffle import Waffle
from itertools import cycle
import pandas as pd
import io
import base64

#Reading data
#Areas Verdes
av = pd.read_csv('bases/areas_verdes.csv')
#Denue
dn = pd.read_csv('bases/DENUE_2020.csv')
dnk1 = pd.read_csv('bases/DENUEK1.csv')

#Inegi 
ine = pd.read_csv('bases/INEGI_2020.csv')
inek1 = pd.read_csv('bases/INEGIK1.csv')

#Denue y Areas Verdes
denAV = pd.read_csv('bases/DenAV.csv')

#Inegi y Areas Verdes
ineAV = pd.read_csv('bases/inegiAV.csv')

#Color palettes
#Paleta de colores y sus variantes
colors = ['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B']
palette = cycle(['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B'])
palet = cycle([ '#4478A6', '#519872', '#A69B8F', '#D4A0A7', '#815E5B', '#F2D544', '#F28907', '#F26B6B', '#B57BA6','#54DEFD'])
palettec = cycle(['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B', '#54DEFD', '#B57BA6', '#D4A0A7', '#A69B8F', '#815E5B'])


#obtener areas verdes de k1 y su porcentaje de m2
avk1 = av[av['SECTOR'] == 'K1']
avk1sum = avk1[['SHAPE_AREA']].sum()
avsum = av[['SHAPE_AREA']].sum()
avPer = (avk1sum/avsum).to_list()
avPer = avPer[0]
avPer = float("{:.2f}".format(avPer))

#porcentaje de poblacion en k1
pobPer = len(inek1.index)/len(ine.index)
pobPer = float("{:.2f}".format(pobPer))

#porcentaje de # servicios en k1
serPer = len(dnk1.index)/len(dn.index)
serPer = float("{:.2f}".format(serPer))
#labels de la legenda
labs = ['Area Verde = '+ str(avPer*100) + '%', 'Poblacion = '+ str(pobPer*100) + '%', 'Servicios = '+ str(avPer*100) + '%']

#grafico de radicales: porcentaje k1
ax = plt.subplot(projection='polar')
ax.barh(0, math.radians(360*avPer), color=colors[1])
ax.barh(1, math.radians(360*pobPer), color=colors[3])
ax.barh(2, math.radians(360*serPer), color=colors[0])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_thetagrids([0, 90, 180, 270], labels=[100, 25, 50, 75])
ax.set_rgrids([])
ax.legend(labels=labs, bbox_to_anchor=(1.00, 1), loc='upper left')
plt.tight_layout()
plt.savefig('matplotfigure.png',dpi=125) # save to the above file object
plt.close()

#Genera # tipos de parque
tip = avk1.groupby('TIPOLOGIA')['NOMBRE_PARQUE'].nunique()

#Grafico de dona: Tipo de Parque
fig2 = go.Figure(go.Pie(labels=tip.index, values=tip.values, hole=.5))
fig2.update_traces(hoverinfo='label+value', textinfo='percent', textfont_size=17, textfont_color="Black", marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
fig2.add_annotation(align="center", text='Total =', showarrow=False, font=dict(size=16, color="Black"))
fig2.add_annotation(align="center", text='<br> <br> <br> 39 Parques', showarrow=False, font=dict(size=20, color="Black"))
fig2.update_layout(width=500,height=500, showlegend=False,hoverlabel=dict(font_size=16, font_color="Black"))

#Limpieza de nombre y crea col Colonia
avk1['DIRECCION'] = avk1['DIRECCION'].str.replace(' ,',',')
col = avk1['DIRECCION'].str.split(",", n = 1, expand = True)
avk1["COLONIA"]= col[0]
#Genera de cuantos tipos de parque tiene cada colonia TOP 8
coltip = avk1.groupby(['COLONIA','TIPOLOGIA']).count()[['NOMBRE_PARQUE']].sort_values(by= ['NOMBRE_PARQUE' ], ascending=False).head(10).unstack(fill_value=0).stack()
# Labels de legenda
categories = ['barrio','bolsillo','lineal','urbano']
#Grafico de araña: Tipo de Paruqe x Colonia TOP 8
fig3 = go.Figure()
for index, new_df in coltip.groupby(level=0):
  fig3.add_trace(go.Scatterpolar(
      r=new_df['NOMBRE_PARQUE'].values,
      theta=categories,
      fill='toself',
      name=new_df.index[1][0],
      line_color=next(palettec)
  ))
fig3.update_layout(
  width=800,
  height=800,
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 12]
    )),
  showlegend=True,
  legend=dict(yanchor='top',xanchor='center')
)

#reset a la paleta para volverse a usar
palettec = cycle(['#4478A6', '#519872', '#F2D544', '#F28907', '#F26B6B', '#54DEFD', '#B57BA6', '#D4A0A7', '#A69B8F', '#815E5B'])
#Genera de cuantos tipos de parque tiene cada colonia
colxtip = avk1.groupby(['COLONIA','TIPOLOGIA']).count()[['NOMBRE_PARQUE']].sort_values(by= ['NOMBRE_PARQUE' ], ascending=False).unstack(fill_value=0).stack()
#Grafico de araña: Tipo de Paruqe x Colonia (TODAS)
fig4 = go.Figure()
for index, new_df in colxtip.groupby(level=0):
  fig4.add_trace(go.Scatterpolar(
      r=new_df['NOMBRE_PARQUE'].values,
      theta=categories,
      fill='toself',
      name=new_df.index[1][0],
      line_color=next(palettec)
  ))
fig4.update_layout(
  width=800,
  height=800,
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 12]
    )),
  showlegend=True,
  legend=dict(yanchor='top',xanchor='center')
)

#Genera # de cada tipo de servicio x Parque
sev = denAV.groupby(['tipo_servicio', 'join_NOMBRE_PARQUE']).count()[['id']].unstack(fill_value=0).stack().sort_values(by='join_NOMBRE_PARQUE')
#Listado de los nombres de los parques con servicios
paq = denAV.sort_values(by='join_NOMBRE_PARQUE')['join_NOMBRE_PARQUE'].unique().tolist()
#Grafico de barra en pila: Ranking de Parques x Servicios
fig5 = go.Figure()
for index, new_df in sev.groupby(level=0):
  fig5.add_trace(go.Bar(
      x=new_df['id'].values,
      y=paq,
      orientation='h',
      name=new_df.index[1][0],
      marker=dict(
        color=next(palet),
        line=dict(color='rgb(250, 250, 250)', width=1)
    )
  ))
fig5.update_xaxes(
        title_text = "# Tipo de Servicios",
        title_font = {"size": 20},
        )
fig5.update_yaxes(
        tickfont=dict(size=8)
        )
fig5.update_traces(hoverinfo="x+name")
fig5.update_layout(barmode='stack', hoverlabel=dict(font_size=16, font_color="White"), width=1200,height=600)

#obtener el total de población de k1 con acceso a y su porcentaje
ineavK1 = ineAV[(ineAV['join_SECTOR'] == 'K1') &(ineAV['distance'] < 0.00261)]
ineavK1sum = ineavK1[['POBTOT']].sum().sum() #doble sum para convertir dtype a float
ineAVsum = ineAV[['POBTOT']].sum().sum() #doble sum para convertir dtype a float
porIAV = int(math.ceil((ineavK1sum/ineAVsum)*10)) #redondea hacia arriba para considerar personas completas
#Grafico de Cuantas personas tienen acceso a un parque a menos de 400 m %
fig6 = plt.figure(
    FigureClass=Waffle,
    rows=2,
    columns=5, 
    values={'Con Acceso': porIAV, 'Sin Acceso':(10-porIAV)},
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
    colors = [colors[1], colors[4]],
    icons='street-view',
    icon_size=50
)
plt.savefig('wafflefigure.png',dpi=125)
plt.close()

#Top 5 parques con mas acceso para la población
topPaq = ineavK1.groupby('NOMBRE_PARQUE').sum()[['POBTOT']].sort_values(by='POBTOT', ascending=False).head(5)
#Grafico de los TOP 5 Parques con mas accesibles a la pob
fig7 = go.Figure()
for index, new_df in topPaq.groupby(level=0):
    fig7.add_trace(go.Bar(
        x=new_df.index,
        y=new_df['POBTOT'].values,
        name=new_df.index[0],
        marker_color=next(palette)
    ))
fig7.update_xaxes(
        showticklabels=False,
        title_text = "Parques",
        title_font = {"size": 18}
        )
fig7.update_layout(
    hoverlabel=dict(font_size=16, font_color="White")
)
fig7.update_traces(hoverinfo="y")


layout = html.Div([

    ####################################### COMIENZA ESPACIO DE EDICIÓN #######################################
#INTRODUCCION
    dbc.Container([
        ## Títutlo
        dbc.Row(
            dbc.Col(
                html.H1('RADIOGRAFÍA URBANA')
            ),className='py-3', style={'background-color': 'black','color': 'white', 'text-align': 'center'}
        ),
        #PONER UNA FOTITO
        ## Texto
        dbc.Row(
            dbc.Col(
                html.H2('¿Qué es el proyecto de Radiografía Urbana?')
            ), className='px-1 py-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H5('Siguiendo con el objetivo principal de IMPLAG sobre desarrollar planes, programas, proyectos estratégicos, políticas publicas y estrategias que fomenten el crecimiento de la ciudad hacia una visión donde sea reconocida por la accesibilidad, seguridad y sustentabilidad es que nace el proyecto Radiografía Urbana en donde se busca obtener un desarrollo urbano dentro del espacio publicó sobresaltando información sobre espacios públicos usables tales como parques, plazas, jardines y demás. San Pedro Garza García en el sector K1')
            ), className='px-1 py-4'
        ),
        html.Iframe(src="../assets/qgis2web_2021_06_08-17_41_26_308204/map.html", style={"height": "600px", "width": "100%"})
         #../qgis2web_2021_06_08-17_41_26_308204/map.html
         #https://www.ons.gov.uk/visualisations/dvc914/map/index.html

    ]),

    ## Contendor con graficas
    dbc.Container([
        ## Títutlo de seccion
        dbc.Row(
            dbc.Col(
                html.H2('Conociendo el área')
            ), className='px-1 pt-4'
        ),
        ## descripción y gráficos
        dbc.Row([
            dbc.Col(
                html.Img(src='../assets/matplotfigure.png', style={'height':'100%', 'width':'100%'}), lg=5, md=4, sm=4
            ),
            dbc.Col(
                html.H5('El sector cuenta con un 17% de poblacion lo cual es mas del doble de las areas verdes que se tienen, la importancia de estos espacios no solo es que ayudan a combatir la contaminación en una ciudad sino también fomenta la vida al aire libre, mejorando la salud física y aumentar la conciencia ambiental.  '), lg=7, md=8, sm=8
            ), 
        ],className='py-3'),
        dbc.Row(
            dbc.Col(
                html.H5('Es importante mencionar que existen diferentes categorías dentro de las mismas areas verdes, parque de bolsillo, lineal, urbano y de barrio. En la gráfica de dona se muestra con mas detalle ')
            ), className='px-1 py-4'
        ),
        dbc.Row(
            dcc.Graph(id='figure2', figure=fig2)
        ),
         ## Títutlo de seccion
        dbc.Row(
            dbc.Col(
                html.H2('Conoce tu colonia ')
            ), className='px-1 pt-4'
        ),
        ## descripción y gráfico
        dbc.Row(
            dbc.Col(
                html.H5('con su respectivo nivel de parques ')
            ), className='px-1 py-4'
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='figure3', figure=fig3)
                #dcc.Graph(id='figure4', figure=fig4)
            )
        ,className='py-3'),
         ## Títutlo de seccion
        dbc.Row(
            dbc.Col(
                html.H2('Accecibilidad')
            ), className='px-1 pt-4'
        ),
        ## descripción y gráfico
        dbc.Row([
            dbc.Col(
                html.Img(src='../assets/wafflefigure.png', style={'height':'100%', 'width':'100%'}), lg=5, md=4, sm=4
            ),
            dbc.Col(
                html.H5('Hoy en día cada 5 personas de 10 tienen acceso a un parque en menos de 400m. La gráfica de barras muestra algunos de los parques más importantes del área y el nivel de accesibilidad que tienen ¿Cuántos de esos partes conoces?'), lg=7, md=8, sm=8
            )
        ],className='py-3'),
        dbc.Row(
            dcc.Graph(id='figure5', figure=fig5)
        ),
        ## Títutlo de seccion
        dbc.Row(
            dbc.Col(
                html.H2('Ranking de Parques')
            ), className='px-1 pt-4'
        ),
        ## descripción y gráfico
        dbc.Row([
            dbc.Col(
                html.H5('El ranking mostrado fue calculado de acuerdo a la cantidad de servicios que se encuentran al rededor haciendo que los visitantes del parque disfruten mas el tiempo al airee libre'), lg=4, md=4, sm=4
            ),
            dbc.Col(
                dcc.Graph(id='figure7', figure=fig7), lg=8, md=8, sm=8
            ), 
        ],className='py-3')
    ]),
    
   
    ######################################## TERMINA ESPACIO DE EDICIÓN ########################################

    # Footer
    dbc.Container([
    
        dbc.Row(
            dbc.Col(
              html.H6('Envíanos un correo a implang@sanpedro.gob.mx')  
            ), className='px-1 pt-4'
        ),

        dbc.Row(
            dbc.Col([
                html.A(
                    html.Img(src='../assets/instagram.png', style={'max-width':'85px', 'height':'34px'}),
                    href='https://www.instagram.com/implang_spgg/', target='blank'
                ),

                html.A(
                    html.Img(src='../assets/facebook.png', style={'max-width':'85px', 'height':'34px'}),
                    href='https://www.facebook.com/implangspgg', target='blank', className='pl-3'
                ),

                html.A(
                    html.Img(src='../assets/twitter.png', style={'max-width':'85px', 'height':'34px'}),
                    href='https://twitter.com/implang_spgg', target='blank', className='pl-3'
                ),

                html.A(
                    html.Img(src='../assets/youtube.png',style={'max-width':'85px', 'height':'34px'}),
                    href='https://www.youtube.com/channel/UCZwYFPh0dHnKhXqzaxlaqNg', target='blank',
                    className='pl-3'
                )
            ]), className='px-1 py-4'
        )
        
    ]),

    dbc.Container([

       dbc.Row(
            dbc.Col(
                html.H6('Instituto Municipal de Planeación y Gestión Urbana')
            ), className='px-1 pt-3'
        ),

        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-1 py-3'
        )
        
    ], style={'background-color': 'black','color': 'white'}
    )
])



