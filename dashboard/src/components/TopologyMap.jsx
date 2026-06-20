import { useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MarkerType,
  applyNodeChanges,
  applyEdgeChanges,
  useNodesState,
  useEdgesState,
  Handle,
  Position
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: 'pot', position: { x: 0, y: 250 }, data: { label: 'Physical Pot & Plant', desc: '8cm Stature / Terracotta Pot' }, type: 'customHardware' },
  { id: 'soil', position: { x: 300, y: 50 }, data: { label: 'Soil Moisture Sensor', desc: 'Reads volumetric water content', tags: [{ icon: '💧', text: 'Moisture' }] }, type: 'customHardware' },
  { id: 'bme', position: { x: 300, y: 250 }, data: { label: 'BME680 (Air)', desc: 'Environmental air quality sensor', tags: [{ icon: '🌡️', text: 'Temp' }, { icon: '💨', text: 'Humidity' }, { icon: '🌫️', text: 'VOCs' }] }, type: 'customHardware' },
  { id: 'lux', position: { x: 300, y: 450 }, data: { label: 'Lux Sensor', desc: 'Measures light intensity (lx)', tags: [{ icon: '☀️', text: 'Light' }] }, type: 'customHardware' },
  { id: 'arduino', position: { x: 620, y: 250 }, data: { label: 'Arduino Uno', desc: 'Hardware aggregation via Firmata' }, type: 'customHardware' },
  { id: 'webcam', position: { x: 920, y: 50 }, data: { label: 'Webcam & Mic', desc: 'Provides visual & acoustic context', tags: [{ icon: '📷', text: 'Vision' }, { icon: '🎤', text: 'Audio' }] }, type: 'customHardware' },
  { id: 'laptop', position: { x: 920, y: 250 }, data: { label: 'Host Laptop', desc: 'Central compute & serial gateway' }, type: 'customHardware' },
  { id: 'owm', position: { x: 920, y: 450 }, data: { label: 'OpenWeatherMaps', desc: 'External forecast API', tags: [{ icon: '⛅', text: 'Forecast' }, { icon: '🌧️', text: 'Rain' }] }, type: 'customCloud' },
  { id: 'pipeline', position: { x: 1240, y: 250 }, data: { label: 'Python Pipeline', desc: 'Data ingestion & preprocessing' }, type: 'customSoftware' },
  { id: 'db', position: { x: 1540, y: 250 }, data: { label: 'SQLite Database', desc: 'Local telemetry persistence' }, type: 'customSoftware' },
  { id: 'claw', position: { x: 1840, y: 250 }, data: { label: 'OpenClaw Agent', desc: 'Autonomous intelligence warden', tags: [{ icon: '🧠', text: 'Memory' }, { icon: '🎭', text: 'Identity' }] }, type: 'customSoftware' },
  { id: 'terminal', position: { x: 1840, y: 450 }, data: { label: 'Host Terminal', desc: 'Direct execution environment' }, type: 'customHardware' },
  { id: 'gemini', position: { x: 2160, y: 50 }, data: { label: 'Gemini Models', desc: 'LLM reasoning engine' }, type: 'customCloud' },
  { id: 'slack', position: { x: 2160, y: 250 }, data: { label: 'Slack', desc: 'Human-in-the-loop notifications' }, type: 'customCloud' },
  { id: 'github', position: { x: 2160, y: 450 }, data: { label: 'GitHub', desc: 'Source & static deployment' }, type: 'customCloud' },
];

const defaultEdgeOptions = {
  type: 'straight',
  animated: true,
  style: { strokeWidth: 2, stroke: 'var(--accent-sage)' },
  markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--accent-sage)' },
};

const initialEdges = [
  { id: 'e1', source: 'pot', target: 'soil', sourceHandle: 'source', targetHandle: 'target', label: 'inserts into dirt', labelBgPadding: [8, 4], labelBgBorderRadius: 4 },
  { id: 'e2', source: 'soil', target: 'arduino', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e3', source: 'bme', target: 'arduino', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e4', source: 'lux', target: 'arduino', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e5', source: 'arduino', target: 'laptop', sourceHandle: 'source', targetHandle: 'target', label: 'Serial over USB', labelBgPadding: [8, 4], labelBgBorderRadius: 4 },
  { id: 'e6', source: 'webcam', target: 'laptop', sourceHandle: 'source', targetHandle: 'target', label: 'USB' },
  { id: 'e7', source: 'owm', target: 'laptop', sourceHandle: 'source', targetHandle: 'target', label: 'JSON API' },
  { id: 'e8', source: 'laptop', target: 'pipeline', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e9', source: 'pipeline', target: 'db', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e10', source: 'db', target: 'claw', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e11', source: 'claw', target: 'terminal', sourceHandle: 'source', targetHandle: 'target', label: 'Bash / Curl' },
  { id: 'e12', source: 'claw', target: 'gemini', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e13', source: 'claw', target: 'slack', sourceHandle: 'source', targetHandle: 'target' },
  { id: 'e14', source: 'claw', target: 'github', sourceHandle: 'source', targetHandle: 'target' },
  
  // Direct Access / On-Demand edges
  { 
    id: 'e-claw-db', source: 'claw', target: 'db', 
    sourceHandle: 'source-bottom', targetHandle: 'target-bottom', 
    type: 'bezier', label: 'Write interpretations & state',
    style: { strokeWidth: 2, stroke: 'var(--accent-sage)', strokeDasharray: '5 5' },
    markerStart: { type: MarkerType.ArrowClosed, color: 'var(--accent-sage)', orient: 'auto-start-reverse' },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--accent-sage)' }
  },
  { 
    id: 'e-claw-arduino', source: 'claw', target: 'arduino', 
    sourceHandle: 'source-bottom', targetHandle: 'target-bottom', 
    type: 'bezier', label: 'Get sensor reading on demand',
    style: { strokeWidth: 2, stroke: 'var(--accent-terracotta)', strokeDasharray: '5 5' },
    markerStart: { type: MarkerType.ArrowClosed, color: 'var(--accent-terracotta)', orient: 'auto-start-reverse' },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--accent-terracotta)' }
  },
  { 
    id: 'e-claw-owm', source: 'claw', target: 'owm', 
    sourceHandle: 'source-top', targetHandle: 'target-top', 
    type: 'bezier', label: 'Fetch forecast on demand',
    style: { strokeWidth: 2, stroke: '#8c968f', strokeDasharray: '5 5' },
    markerStart: { type: MarkerType.ArrowClosed, color: '#8c968f', orient: 'auto-start-reverse' },
    markerEnd: { type: MarkerType.ArrowClosed, color: '#8c968f' }
  },
  { 
    id: 'e-claw-webcam', source: 'claw', target: 'webcam', 
    sourceHandle: 'source-top', targetHandle: 'target-top', 
    type: 'bezier', label: 'Get photo when in doubt',
    style: { strokeWidth: 2, stroke: 'var(--accent-terracotta)', strokeDasharray: '5 5' },
    markerStart: { type: MarkerType.ArrowClosed, color: 'var(--accent-terracotta)', orient: 'auto-start-reverse' },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'var(--accent-terracotta)' }
  }
];

const CustomNode = ({ data, typeColor, bgColor, borderStyle = 'solid', isConnectable }) => (
  <div style={{
    padding: '12px 14px',
    borderRadius: '12px',
    background: bgColor,
    border: `2px ${borderStyle} ${typeColor}`,
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
    color: 'var(--text-primary)',
    textAlign: 'center',
    minWidth: '220px',
    maxWidth: '220px',
    fontFamily: 'var(--font-sans)',
    position: 'relative'
  }}>
    <Handle id="target-top" type="target" position="top" isConnectable={isConnectable} style={{ visibility: 'hidden' }} />
    <Handle id="source-top" type="source" position="top" isConnectable={isConnectable} style={{ visibility: 'hidden' }} />
    <Handle id="target-bottom" type="target" position="bottom" isConnectable={isConnectable} style={{ visibility: 'hidden' }} />
    <Handle id="source-bottom" type="source" position="bottom" isConnectable={isConnectable} style={{ visibility: 'hidden' }} />
    <Handle id="target" type="target" position="left" isConnectable={isConnectable} style={{ background: typeColor, width: 8, height: 8 }} />
    
    <div style={{ fontWeight: 600, fontSize: '16.5px', marginBottom: data.desc ? '4px' : '0', lineHeight: '1.2' }}>{data.label}</div>
    {data.desc && <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: data.tags ? '10px' : '0', lineHeight: '1.2' }}>{data.desc}</div>}
    
    {data.tags && (
      <div style={{ display: 'flex', gap: '4px', justifyContent: 'center', flexWrap: 'wrap', marginTop: '6px' }}>
        {data.tags.map((tag, i) => (
          <div key={i} style={{
            background: 'var(--surface-bg)',
            border: '1px solid var(--surface-border)',
            padding: '2px 6px',
            borderRadius: '6px',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            color: 'var(--text-primary)',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
          }}>
            <span>{tag.icon}</span>
            <span style={{ fontWeight: 500 }}>{tag.text}</span>
          </div>
        ))}
      </div>
    )}

    <Handle id="source" type="source" position="right" isConnectable={isConnectable} style={{ background: typeColor, width: 8, height: 8 }} />
  </div>
);

const nodeTypes = {
  customHardware: (props) => <CustomNode {...props} typeColor="var(--accent-terracotta)" bgColor="#faf8f5" />,
  customSoftware: (props) => <CustomNode {...props} typeColor="var(--accent-sage)" bgColor="#ffffff" />,
  customCloud: (props) => <CustomNode {...props} typeColor="#8c968f" bgColor="#f4f1ea" borderStyle="dashed" />,
};

export default function TopologyMap() {
  const [nodes, setNodes] = useNodesState(initialNodes);
  const [edges, setEdges] = useEdgesState(initialEdges);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  return (
    <div className="glass-panel" style={{ height: '80vh', width: '100%', position: 'relative', overflow: 'hidden' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        defaultEdgeOptions={defaultEdgeOptions}
        fitView
        attributionPosition="bottom-right"
      >
        <Background color="#ccc" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
