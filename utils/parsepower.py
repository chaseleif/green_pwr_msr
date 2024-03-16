#! /usr/bin/env python3

import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# https://github.com/plotly/Kaleido/issues/122
import plotly.io as pio
pio.kaleido.scope.mathjax = None

# if there were some kind of common pre-processing/etc to do . . .
def powerstats(powercsv):
  df = pd.read_csv(powercsv)
  return df

def plotstats(**kwargs):
  # Default plot-level arguments, overridden by kwargs
  args = {'font':{'size':18},
          'title':{ 'text':'Power Usage','automargin':True,'yref':'container',
                    'xanchor':'center','yanchor':'top','x':0.48,'y':0.95},
          'legend':{'yanchor':'top','xanchor':'right','y':0.99,'x':0.99},
          'xtitle':'Runtime (s)',
          'ytitle':'Power',
          'traces':{'marker_line_width':2,
                    'marker_size':10},
          'bgcolor':'white',
          'savefile':None}
  args.update(kwargs)
  # default csv args ~ missing 'filename'
  csvargs = { 'legendname':'Power',
              'xcol':'timestamp',
              'ycol':'power',
              'scattermode':'markers+lines',
              'avgline':True,
              'maxarrow':True,
              'marker':{'color':'black'} }
  fig = go.Figure()
  fig.update_xaxes(gridcolor='lightgray', griddash='dash')
  fig.update_yaxes(gridcolor='lightgray', griddash='dash')
  for csv in sorted([key for key in args.keys() if key.startswith('csv')]):
    csv = args[csv]
    csv.update({key:val for key,val in csvargs.items() if key not in csv})
    df = powerstats(csv['filename'])
    if csv['avgline']:
      avg = df[csv['ycol']].mean()
      fig.add_trace(go.Scatter( name=f'Average {csv["legendname"]}',
                                x=df[csv['xcol']],
                                y=[avg for _ in range(df.shape[0])],
                                mode='lines'))
      fig.update_traces(marker_line_width=2, marker_size=8)
    fig.add_trace(go.Scatter( name=csv['legendname'],
                              x=df[csv['xcol']],
                              y=df[csv['ycol']],
                              mode=csv['scattermode'],
                              marker=csv['marker'],
                              text=[str(round(val,2)) \
                                    for val in df[csv['ycol']].values],
                              textposition='bottom center'))
    if csv['maxarrow']:
      maxy = df['power'].max()
      maxx = df[df['power']==maxy]['timestamp'].values[0]
      fig.add_annotation(x=maxx, y=maxy,
                          text=str(round(maxy,2)),
                          showarrow=True,
                          arrowhead=0)
  fig.update_traces(**args['traces'])
  fig.update_layout(title=args['title'],
                    xaxis_title=args['xtitle'],
                    yaxis_title=args['ytitle'],
                    font=args['font'],
                    legend=args['legend'],
                    plot_bgcolor=args['bgcolor'])
  if args['savefile'] is not None:
    fig.write_image(args['savefile'])
  else:
    fig.show()

if __name__ == '__main__':
  if len(sys.argv) == 2:
    plotstats(csv={ 'filename':sys.argv[1],
                    'marker':{'color':'darkgreen'} })
  elif len(sys.argv) == 3:
    plotstats(savefile='powerfig.pdf',
              csv1={'filename':sys.argv[1],
                    'marker':{'color':'lightblue'},
                    'legendname':Path(sys.argv[1]).stem.title(),
                    'avgline':False},
              csv2={'filename':sys.argv[2],
                    'marker':{'color':'darkgreen'},
                    'legendname':Path(sys.argv[2]).stem.title(),
                    'avgline':False})
  else:
    print(f'{sys.argv[0]} - requires a csv argument')
    print('Plots a csv, and, optionally, 2 csvs for comparison')
    print('Usage:')
    print(f'python3 {sys.argv[0]} poweruse.csv [other.csv]')

