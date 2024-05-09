from .file_associations import *
from .transform import *
class shapeManager:
    def __init__(self,directory=None):
        self.shapes_repository = {}
        self.dataDir = directory
        self.directories=self.get_directories()
        self.land_mgr = landManager(self.directories)
    def get_geo_data_dir(self,subDir=None):
        dataDir = self.dataDir
        if subDir:
            dataDir= os.path.join(self.dataDir,subDir)
        return dataDir
    def get_directories(self):
        directories = {'zipcodes':"",'cities':"",'counties':""}
        for designation,value in directories.items():
            directories[designation]=self.get_geo_data_dir(subDir=designation)
        return directories
    def get_contents(self,dir_name,file_type,update=None):
        contents = self.shapes_repository.get(dir_name,{}).get(file_type)
        if contents is None or (update is not None and not isinstance(update,bool)):
            contents = self.land_mgr.get_contents(dir_name=dir_name,file_type=file_type,update=update)
            dir_name = str(dir_name)
            if contents is not None:
                if dir_name not in self.shapes_repository:
                    self.shapes_repository[dir_name] = {}
                if file_type not in self.shapes_repository[dir_name]:
                    self.shapes_repository[dir_name][file_type]=None
                contents = contents.to_crs(epsg=4326)
                self.shapes_repository[dir_name][file_type]=contents
        return self.shapes_repository[dir_name][file_type]
    def get_polygon(self,designation,value):
        designation = get_closest_designation(designation)
        column_name = get_column_name(designation)
        geo_df = shape_mgr.get_contents(designation,'shp')
        return self.land_mgr.get_polygon(geo_df,column_name,value)
    def get_column_name(self,designation,file_type='shp'):
        designation = get_closest_designation(designation)
        column_keys = get_column_js().get(designation)
        geo_df = self.get_contents(designation,file_type)
        column_name = [name for name in geo_df.columns.tolist() if name in column_keys]
        if column_name and isinstance(column_name,list) and len(column_name)>0:
            return column_name[0]
        return column_keys_js[designation][0]
    def get_column_list(self,designation,file_type='shp'):
        column_name = get_column_name(designation,file_type)
        geo_df = self.get_contents(designation,file_type)
        if geo_df is not None:
            return geo_df[column_name].tolist()
