CREATE OR REPLACE FUNCTION notify_py_client() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('fhir_db_trigger_rtd', json_build_object('operation', TG_OP, 'id', NEW.res_id,'type', NEW.res_type,'deleted',NEW.res_deleted_at)::text);
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER notify_python_client AFTER INSERT OR UPDATE ON hfj_resource FOR EACH ROW EXECUTE PROCEDURE notify_py_client();