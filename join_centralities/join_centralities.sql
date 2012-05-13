-- Creates a view of the total centrality for each professor, by joining the authorship table with a table containing the papers' calculated centralies.
-- With the calculated centralities for the papers in the table "centralities" in the SQLite db, run this SQL.
-- Set the field names for the relevant centrality and professor-measure.
DROP VIEW IF EXISTS professor_measure_blah;
CREATE VIEW professor_measure_blah AS
    SELECT year, ucpay_id, SUM(some_centrality)
    FROM paper_authorship INNER JOIN centralities USING (some_centrality)
    GROUP BY (year, ucpay_id)
;