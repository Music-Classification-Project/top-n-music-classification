
import React from 'react';
import { useParams } from 'react-router-dom';
import { RadialBarChart, PolarAngleAxis, RadialBar } from 'recharts';

const RadialChart = () => {
    const predictions = useParams()
    let predict = JSON.parse(predictions.predictions)
    predict = predict['predictions']
    predict.sort((a, b) => a.confidence - b.confidence);
    console.log(predict)
    

  return (
    <RadialBarChart width={500} height={500} data={predict}
    innerRadius="20%"
    barSize={4}
    startAngle={90}
    endAngle={-270}>
      <PolarAngleAxis
        type="number"
        domain={[0, 1]}
        angleAxisId={0}
        tick={false}
      />
     <RadialBar
       minAngle={30} dataKey='confidence' name='genre' label
      />
      <text
        x={500 / 2}
        y={500 / 2}
        textAnchor="middle"
        dominantBaseline="middle"
        className="progress-label">
        Test
      </text>
    </RadialBarChart>
  );
};

export default RadialChart;
