# graph-experiment

Playing with MTA data to keep myself refreshed on graph theory.

1. Define modeling assumptions
2. Load GTFS data
3. Construct stops and routes
4. Build graph w typed edges (line vs transfer edge)
5. Infer and attach transfer edges
6. Validate graph (counts, connectivity)
7. Derive graph-based features (degree, betweenness centrality, connectivity, cut-edges)
8. Edge impact regression
9. Evaluate and analyze failure cases

## Modeling Assumptions

1. Nodes are defined at the station level
2. Trip edges connect consecutive stops along a route, and are directed
3. Transfer edges connect stops within the same station where transfers are possible, and are bidirectional
4. Express/local tracks are modeled separately
5. Trip edges are weighted based on trip time. For the initial edge in a trip, service frequency is also factored into the weight
6. Transfer edges are weighted based on one of two static average transfer times, for either same-platform or different-platform transfers
7. Only daytime weekday service will be considered initially; edges will store applicable service_ids for potential filtering in future analyses
8. The graph will provide a static snapshot of service; exact departure/arrival times will not be modeled
9. Limitations: service disruptions, non-MTA connected services, and unofficial transfers are excluded
10. Edge removal simulates complete service disruption; partial reduction is not modeled