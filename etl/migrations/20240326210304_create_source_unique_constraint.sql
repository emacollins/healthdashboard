-- Add migration script here
ALTER TABLE sources ADD CONSTRAINT unique_source UNIQUE (source_name, device_name, device_manufacturer, device_model, device_hardware, device_software);