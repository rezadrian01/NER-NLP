"""
Flask Web Application for Wayang Knowledge Graph Explorer
Author: Ahmad Reza Adrian

This module provides a web interface for exploring the wayang knowledge graph.
"""

import json
import logging
from pathlib import Path

from flask import Flask, render_template, jsonify, request, send_file

from config import OUTPUT_DIR, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from pipeline import WayangPipeline

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Global pipeline instance
pipeline = None


def init_pipeline():
    """Initialize the pipeline if not already done."""
    global pipeline
    if pipeline is None:
        logger.info("Initializing pipeline...")
        pipeline = WayangPipeline()
        
        # Check if processed data exists
        json_path = Path(OUTPUT_DIR) / "knowledge_graph.json"
        if json_path.exists():
            logger.info("Loading existing knowledge graph...")
            pipeline.knowledge_graph.from_json(str(json_path))
        else:
            logger.info("No existing graph found. Please run the pipeline first.")
    
    return pipeline


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/graph')
def get_graph():
    """API endpoint to get the complete graph data."""
    try:
        p = init_pipeline()
        
        if p.knowledge_graph.graph.number_of_nodes() == 0:
            return jsonify({
                'error': 'No graph data available. Please run the pipeline first.'
            }), 404
        
        # Get graph data
        graph_data = p.knowledge_graph.to_json()
        
        return jsonify(graph_data)
    
    except Exception as e:
        logger.error(f"Error getting graph: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/entity/<entity_name>')
def get_entity(entity_name):
    """API endpoint to get entity information."""
    try:
        p = init_pipeline()
        
        entity_info = p.get_entity_info(entity_name)
        
        if entity_info is None:
            return jsonify({
                'error': f'Entity "{entity_name}" not found'
            }), 404
        
        return jsonify(entity_info)
    
    except Exception as e:
        logger.error(f"Error getting entity: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """API endpoint to get graph statistics."""
    try:
        p = init_pipeline()
        
        stats = p.knowledge_graph.get_statistics()
        
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search')
def search_entities():
    """API endpoint to search for entities."""
    try:
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify({'results': []})
        
        p = init_pipeline()
        
        # Search in node names
        results = []
        for node, data in p.knowledge_graph.graph.nodes(data=True):
            if query in node.lower():
                results.append({
                    'name': node,
                    'type': data.get('type', 'UNKNOWN'),
                    'count': data.get('count', 0)
                })
        
        return jsonify({'results': results})
    
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/visualization')
def visualization():
    """Serve the graph visualization page."""
    html_path = Path(OUTPUT_DIR) / "knowledge_graph.html"
    
    if html_path.exists():
        return send_file(str(html_path))
    else:
        return "Visualization not found. Please run the pipeline first.", 404


@app.route('/entity/<entity_name>')
def entity_detail(entity_name):
    """Entity detail page."""
    return render_template('entity.html', entity_name=entity_name)


@app.route('/api/entity/<entity_name>/visualization')
def generate_entity_visualization(entity_name):
    """Generate 1-level visualization for a specific entity."""
    try:
        p = init_pipeline()
        
        if not p.knowledge_graph.graph.has_node(entity_name):
            return jsonify({
                'error': f'Entity "{entity_name}" not found'
            }), 404
        
        # Generate visualization using the new method
        from visualization import GraphVisualizer
        
        visualizer = GraphVisualizer()
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)
        
        safe_name = entity_name.replace(' ', '_').lower()
        html_path = output_dir / f"entity_{safe_name}.html"
        
        visualizer.visualize_entity_direct_relations(
            p.knowledge_graph,
            entity_name,
            output_path=str(html_path)
        )
        
        return jsonify({
            'success': True,
            'path': str(html_path),
            'url': f'/entity/{entity_name}/graph'
        })
    
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/entity/<entity_name>/graph')
def entity_visualization(entity_name):
    """Serve the entity-specific visualization."""
    try:
        p = init_pipeline()
        
        # Check if knowledge graph is loaded
        if p.knowledge_graph.graph.number_of_nodes() == 0:
            return f"<h1>Error</h1><p>Knowledge graph is empty. Please run the pipeline first: <code>python pipeline.py</code></p>", 404
        
        # Check if entity exists
        if not p.knowledge_graph.graph.has_node(entity_name):
            return f"<h1>Entity Not Found</h1><p>Entity '{entity_name}' does not exist in the knowledge graph.</p><p><a href='/'>Back to Home</a></p>", 404
        
        # Check if visualization already exists
        safe_name = entity_name.replace(' ', '_').lower()
        html_path = Path(OUTPUT_DIR) / f"entity_{safe_name}.html"
        
        if html_path.exists():
            return send_file(str(html_path))
        
        # Generate visualization
        from visualization import GraphVisualizer
        
        visualizer = GraphVisualizer()
        visualizer.visualize_entity_direct_relations(
            p.knowledge_graph,
            entity_name,
            output_path=str(html_path)
        )
        
        return send_file(str(html_path))
        
    except Exception as e:
        logger.error(f"Error in entity_visualization: {e}", exc_info=True)
        return f"<h1>Error</h1><p>Failed to generate visualization: {str(e)}</p><p><a href='/'>Back to Home</a></p>", 500


def create_templates():
    """Create template HTML files."""
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Index template
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wayang Knowledge Graph Explorer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 40px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white;
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }
        .btn:hover {
            background: white;
            color: #667eea;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
        }
        .stat-label {
            opacity: 0.9;
            margin-top: 5px;
        }
        #search-box {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }
        #search-results {
            margin-top: 20px;
        }
        .result-item {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .result-item:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: translateX(5px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Wayang Knowledge Graph Explorer</h1>
        <p class="subtitle">Explore Indonesian wayang stories through named entities and their relationships</p>
        
        <div class="card">
            <h2>Graph Statistics</h2>
            <div class="stats-grid" id="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="stat-nodes">-</div>
                    <div class="stat-label">Entities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="stat-edges">-</div>
                    <div class="stat-label">Relations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="stat-density">-</div>
                    <div class="stat-label">Density</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Visualization</h2>
            <p>View the interactive knowledge graph with all entities and their relationships.</p>
            <a href="/visualization" class="btn" target="_blank">Open Graph Visualization</a>
        </div>
        
        <div class="card">
            <h2>Search Entities</h2>
            <input type="text" id="search-box" placeholder="Search for wayang characters, places, events...">
            <div id="search-results"></div>
        </div>
    </div>
    
    <script>
        // Load statistics
        fetch('/api/statistics')
            .then(response => response.json())
            .then(data => {
                document.getElementById('stat-nodes').textContent = data.total_nodes || 0;
                document.getElementById('stat-edges').textContent = data.total_edges || 0;
                document.getElementById('stat-density').textContent = (data.density || 0).toFixed(3);
            })
            .catch(error => console.error('Error loading statistics:', error));
        
        // Search functionality
        let searchTimeout;
        document.getElementById('search-box').addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            const query = e.target.value;
            
            if (query.length < 2) {
                document.getElementById('search-results').innerHTML = '';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                fetch(`/api/search?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        const resultsDiv = document.getElementById('search-results');
                        
                        if (data.results && data.results.length > 0) {
                            resultsDiv.innerHTML = data.results.map(entity => `
                                <div class="result-item" onclick="viewEntity('${entity.name}')">
                                    <strong>${entity.name}</strong> 
                                    <span style="opacity: 0.8;">[${entity.type}]</span>
                                    <span style="opacity: 0.7; float: right;">Mentions: ${entity.count}</span>
                                </div>
                            `).join('');
                        } else {
                            resultsDiv.innerHTML = '<p style="opacity: 0.7;">No results found</p>';
                        }
                    })
                    .catch(error => console.error('Error searching:', error));
            }, 300);
        });
        
        function viewEntity(entityName) {
            // Redirect to 1-level graph visualization directly
            window.location.href = `/entity/${encodeURIComponent(entityName)}/graph`;
        }
    </script>
</body>
</html>"""
    
    # Entity template
    entity_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entity: {{ entity_name }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .back-btn, .viz-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid white;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            display: inline-block;
            margin-right: 10px;
            transition: all 0.3s;
        }
        .back-btn:hover, .viz-btn:hover {
            background: white;
            color: #667eea;
        }
        .viz-btn {
            background: rgba(76, 175, 80, 0.3);
            border-color: #4caf50;
        }
        .viz-btn:hover {
            background: #4caf50;
            color: white;
        }
        .relation-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 15px;
            border-radius: 8px;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="margin-bottom: 20px;">
            <a href="/" class="back-btn">← Back to Home</a>
            <a href="/entity/{{ entity_name }}/graph" class="viz-btn" target="_blank">🎨 View Graph (1-Level)</a>
        </div>
        <h1 id="entity-name">{{ entity_name }}</h1>
        <div id="entity-info"></div>
    </div>
    
    <script>
        const entityName = "{{ entity_name }}";
        
        fetch(`/api/entity/${encodeURIComponent(entityName)}`)
            .then(response => response.json())
            .then(data => {
                const infoDiv = document.getElementById('entity-info');
                
                infoDiv.innerHTML = `
                    <div class="card">
                        <h2>Information</h2>
                        <p><strong>Type:</strong> ${data.type}</p>
                        <p><strong>Mentions:</strong> ${data.mention_count}</p>
                        <p><strong>Connections:</strong> ${data.degree}</p>
                    </div>
                    
                    <div class="card">
                        <h2>Outgoing Relations</h2>
                        ${data.outgoing_relations.map(rel => `
                            <div class="relation-item">
                                ${data.name} → <strong>${rel.relations.join(', ')}</strong> → ${rel.target}
                            </div>
                        `).join('') || '<p>No outgoing relations</p>'}
                    </div>
                    
                    <div class="card">
                        <h2>Incoming Relations</h2>
                        ${data.incoming_relations.map(rel => `
                            <div class="relation-item">
                                ${rel.source} → <strong>${rel.relations.join(', ')}</strong> → ${data.name}
                            </div>
                        `).join('') || '<p>No incoming relations</p>'}
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error loading entity:', error);
                document.getElementById('entity-info').innerHTML = 
                    '<div class="card"><p>Error loading entity information</p></div>';
            });
    </script>
</body>
</html>"""
    
    # Write templates
    (templates_dir / "index.html").write_text(index_html, encoding='utf-8')
    (templates_dir / "entity.html").write_text(entity_html, encoding='utf-8')
    
    logger.info(f"Templates created in {templates_dir}")


def main():
    """Run the Flask application."""
    # Create templates
    create_templates()
    
    # Initialize pipeline
    init_pipeline()
    
    # Run Flask app
    logger.info(f"Starting Flask server at http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == "__main__":
    main()
