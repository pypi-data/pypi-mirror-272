from .file_associations import *
from .transform import *
import logging
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
# Setup logging
def get_latitude_longitude(point_js):
    point_js['latitude']=False
    if str(point_js.get('direction')).lower() in ['north','south','true']:
        point_js['latitude']=True
    return point_js
logging.basicConfig(level=logging.INFO)
def check_and_convert_epsg(gdf: gpd.GeoDataFrame, epsg: int = 4326) -> gpd.GeoDataFrame:
    """
    Ensure the GeoDataFrame is in the specified EPSG code.
    
    Parameters:
    - gdf (gpd.GeoDataFrame): Input GeoDataFrame.
    - epsg (int): Target EPSG code.
    
    Returns:
    - gpd.GeoDataFrame: GeoDataFrame in the target CRS.
    """
    try:
        # Check if CRS exists and matches the desired EPSG
        current_epsg = gdf.crs.to_epsg() if gdf.crs else None

        if current_epsg is None:
            # If CRS is missing, assign the desired EPSG directly
            logging.info(f"No CRS assigned, setting directly to EPSG:{epsg}")
            gdf.set_crs(epsg=epsg, inplace=True)
        elif current_epsg != epsg:
            # Convert CRS if necessary
            logging.info(f"Converting CRS from EPSG:{current_epsg} to EPSG:{epsg}")
            gdf = gdf.to_crs(epsg=epsg)
        else:
            # CRS is already correct
            logging.info(f"GeoDataFrame is already in EPSG:{epsg}")
    except Exception as e:
        logging.error(f"Error checking/converting CRS: {e}")

    return gdf

class shapeManager(metaclass=SingletonMeta):
    def __init__(self, directory=None,epsg=4326):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.shapes_repository = {}
            self.dataDir = directory
            self.directories = self.get_directories()
            self.land_mgr = landManager(self.directories)
            self.epsg = epsg
def get_contents(self, dir_name, file_type, epsg=4326, update=None):
    logging.info(f"Fetching contents for directory: {dir_name}, file type: {file_type}")
    try:
        # Retrieve cached contents if available
        contents = self.shapes_repository.get(dir_name, {}).get(file_type)

        if contents is None or (update is not None and not isinstance(update, bool)):
            # Retrieve fresh data
            contents = self.land_mgr.get_contents(dir_name=dir_name, file_type=file_type, update=update)
            dir_name = str(dir_name)

            if contents is not None:
                # Cache the data
                if dir_name not in self.shapes_repository:
                    self.shapes_repository[dir_name] = {}

                if file_type not in self.shapes_repository[dir_name]:
                    self.shapes_repository[dir_name][file_type] = None

                # Ensure data has the correct EPSG code
                contents = check_and_convert_epsg(contents, epsg=epsg)

                # Cache the transformed data
                self.shapes_repository[dir_name][file_type] = contents

                logging.info(f"Contents fetched and transformed to EPSG:{epsg} for directory: {dir_name}, file type: {file_type}")
                return contents
        else:
            # Return cached contents
            logging.info(f"Returning cached contents for directory: {dir_name}, file type: {file_type}")
            return contents
    except Exception as e:
        logging.error(f"Error fetching contents for directory: {dir_name}, file type: {file_type}: {e}")
        return None

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
        else:
            return contents
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
    def get_derived_geom(self,point_js):
        designation,value= get_city_or_county(point_js)
        df_a = self.get_contents(designation,'shp')
        geom = get_any_geom(df_a,designation,column=self.get_column_name(designation,file_type='shp'))
        if point_js.get('from') == 'center':
            geom = geom.centroid
        point_js['geom']=geom
        return point_js
    def derive_cardinal_vars(self,point_js):
        point_js= self.get_derived_geom(point_js)
        point_js = get_latitude_longitude(point_js)
        point_js['rangeInclusive'] = str(point_js.get('rangeInclusive')).lower() == 'false'
        return point_js
        
