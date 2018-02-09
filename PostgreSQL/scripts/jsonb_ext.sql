
-- jsonb de-duplicate json array
CREATE OR REPLACE FUNCTION jsonb_usedef_dedup(arg JSONB) RETURNS JSONB AS 
$$
DECLARE
    res JSONB;
begin
	with in_test as
	(
	select distinct(jsonb_array_elements(arg)) as jsobj
	)
	
	 select jsonb_agg(jsobj) into res from in_test;
	 return res;
end;
$$ LANGUAGE plpgsql immutable SECURITY DEFINER

-- jsonb aggregate concat 
CREATE AGGREGATE jsonb_object_agg(jsonb) (  
  SFUNC = 'jsonb_concat',
  STYPE = jsonb,
  PARALLEL = SAFE
);
