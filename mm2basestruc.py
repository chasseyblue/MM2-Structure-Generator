import csv
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from vp_setup_ui import Ui_MainWindow
from PyQt5.QtGui import QIcon

class VehicleFolderSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the OK button to the functionality
        self.ui.okButton.clicked.connect(self.on_submit)

        # Supply icon to MainWindow
        self.setWindowIcon(QIcon("_internal\\vpgen.ico"))

    def on_submit(self):
        # Get input values from the fields
        vehicle_name = self.ui.vehicleNameInput.text().strip()
        description = self.ui.descriptionInput.text().strip()
        variations = self.ui.variationsInput.text().strip()

        # Validate inputs
        if not vehicle_name:
            QMessageBox.warning(self, "Input Required", "Please enter the base vehicle name.")
            return
        if not description:
            QMessageBox.warning(self, "Input Required", "Please enter the vehicle description.")
            return
        if not variations:
            QMessageBox.warning(self, "Input Required", "Please enter the colors (variations).")
            return

        # Process variations (colours) into a single string
        colors = "|".join([v.strip() for v in variations.split("|") if v.strip()])

        # Base path (including sub folders)
        base_path = os.path.join(os.getcwd(), vehicle_name)
        tune_folder_path = os.path.join(base_path, "tune")
        vehicle_folder_path = os.path.join(tune_folder_path, "vehicle")
        camera_folder_path = os.path.join(tune_folder_path, "camera")
        banger_folder_path = os.path.join(tune_folder_path, "banger")
        folders = [
            f"{base_path}\\aud\\aud22\\engines",
            f"{base_path}\\aud\\aud22\\horns",
            f"{base_path}\\aud\\cardata\\opponent",
            f"{base_path}\\aud\\cardata\\player",
            f"{base_path}\\bound",
            f"{base_path}\\geometry",
            f"{base_path}\\jpg",
            f"{base_path}\\texture",
            tune_folder_path,
            vehicle_folder_path,
            banger_folder_path,
            camera_folder_path,
        ]

        # Create folder structure
        try:
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create folder structure: {e}")
            return

        # File generation functions
        # tune\ .info
        def generate_info_file():
            info_file_path = os.path.join(tune_folder_path, f"{vehicle_name}.info")
            content = (
                f"BaseName={vehicle_name}\n"
                f"Description={description}\n"
                f"Colors={colors}\n"
                "Flags=0\n"
                "Order=-1\n"
                "ScoringBias=0\n"
                "UnlockScore=0\n"
                "UnlockFlags=0\n"
                "Horsepower=380\n"
                "Top Speed=148\n"
                "Durability=700000\n"
                "Mass=2975\n"
                "UIDist=5.5\n"
                "LockColorMask=0\n"
                "ForceFeedbackModifier=1.0\n"
                "RoadForceModifier=2.0\n"
            )
            with open(info_file_path, "w") as file:
                file.write(content)
            return info_file_path

        # tune\ .asNode
        def generate_asnode_file():
            asnode_file_path = os.path.join(tune_folder_path, f"{vehicle_name}.asNode")
            content = (
                "type: a\n"
                "asNode {\n"
                "  SpeedSensitive 2\n"
                "  SpeedBaseLow 5.000000\n"
                "  MouseSensitivityLow 0.899999\n"
                "  MouseSteerFilterLow 0.500000\n"
                "}\n"
            )
            with open(asnode_file_path, "w") as file:
                file.write(content)
            return asnode_file_path

        # tune\ .mmMirror
        def generate_mm_mirror_file():
            mm_mirror_file_path = os.path.join(tune_folder_path, f"{vehicle_name}.mmMirror")
            content = (
                "type: a\n"
                "mmMirror {\n"
                "  Position 0.000000 1.400000 -1.000000\n"
                "  Size 0.300000 0.160000\n"
                "  Fov 10.000000\n"
                "}\n"
            )
            with open(mm_mirror_file_path, "w") as file:
                file.write(content)
            return mm_mirror_file_path

        # tune\ _dash.AsNode
        def generate_dash_asnode_file():
            dash_asnode_file_path = os.path.join(tune_folder_path, f"{vehicle_name}_dash.asNode")
            content = (
                "type: a\n"
                "asNode {\n"
                "  DashPos 0.110300 -0.610800 -0.800400\n"
                "  RoofPos 0.095600 -0.519000 -0.800100\n"
                "}\n"
            )
            with open(dash_asnode_file_path, "w") as file:
                file.write(content)
            return dash_asnode_file_path

        # tune\vehicle\ .vehCarDamage
        def generate_veh_cardamage_file():
            veh_cardamage_file_path = os.path.join(vehicle_folder_path, f"{vehicle_name}.vehCarDamage")
            content = (
                "type: a\n"
                "vehCarDamage {\n"
                "  MaxDamage 343750.000000\n"
                "  MedDamage 287500.000000\n"
                "  ImpactThreshold 1500.000000\n"
                "  RegenerateRate 0.000000\n"
                "  SmokeOffset -0.450000 0.780000 -1.970000\n"
                "  TextelDamageRadius 3.000000\n"
                "}\n"
            )
            with open(veh_cardamage_file_path, "w") as file:
                file.write(content)
            return veh_cardamage_file_path
        
        # tune\vehicle\ .vehCarSim
        def generate_veh_carsim_file():
            veh_carsim_file_path = os.path.join(vehicle_folder_path, f"{vehicle_name}.vehcarsim")
            content = (
                "type: a\n"
                "vehCarSim {\n"
                "  Mass 1300.000000\n"
                "  InertiaBox 2.500000 2.000000 5.000000\n"
                "  CenterOfGravity 0.000000 -0.100000 0.150000\n"
                "  BoundFriction 0.300000\n"
                "  BoundElasticity 0.500000\n"
                "  DrivetrainType 0\n"
                "  SSSValue 1.000000\n"
                "  SSSThreshold 0.000000\n"
                "  CarFrictionHandling 1.000000\n"
                "  Aero {\n"
                "    AngCDamp 2.000000 5.000003 3.000000\n"
                "    AngVelDamp 0.000000 0.000000 0.000000\n"
                "    AngVel2Damp 0.000000 5.000006 1.999999\n"
                "    Drag 0.300000\n"
                "    Down 0.000000\n"
                "  }\n"
                "  Engine {\n"
                "    AngInertia 1.000000\n"
                "    MaxHorsePower 550.000000\n"
                "    IdleRPM 750.000000\n"
                "    OptRPM 6128.000000\n"
                "    MaxRPM 7615.000000\n"
                "    GCL 0.250000\n"
                "  }\n"
                "  Trans {\n"
                "    ManualNumGears 6\n"
                "    AutoNumGears 6\n"
                "    Reverse 30.000000\n"
                "    Low 30.000000\n"
                "    High 110.000000\n"
                "    GearBias 0.500000\n"
                "    UpshiftBias 0.050000\n"
                "    DownshiftBiasMin 0.050000\n"
                "    DownshiftBiasMax 0.300000\n"
                "    GearChangeTime 1.000000\n"
                "  }\n"
                "  Drivetrain {\n"
                "    AngInertia 4460.000000\n"
                "    BrakeDynamicCoef 1.000000\n"
                "    BrakeStaticCoef 1.200000\n"
                "  }\n"
                " Freetrain {\n"
                "   AngInertia 2000.000000\n"
                "   BrakeDynamicCoef 1.000000\n" 
                "   BrakeStaticCoef 1.200000\n"
                " }\n"
                " WheelFront {\n"
                "   SuspensionExtent 0.200000\n"
                "   SuspensionLimit 0.100000\n"
                "   SuspensionFactor 1.300000\n" 
                "   SuspensionDampCoef 0.020000\n"
                "   SteeringLimit 0.400000\n"
                "   SteeringOffset 0.260000\n"
                "   BrakeCoef 0.400000\n"
                "   HandbrakeCoef 2.000000\n"
                "   CamberLimit 0.409000\n"
                "   WobbleLimit 0.000000\n"
                "   TireDispLimitLong 0.125000\n"
                "   TireDampCoefLong 0.250000\n"
                "   TireDragCoefLong 0.020000\n"
                "   TireDispLimitLat 0.125000\n"
                "   TireDampCoefLat 0.250000\n"
                "   TireDragCoefLat 0.050000\n"
                "   OptimumSlipPercent 0.20000\n" 
                "   StaticFric 3.000000\n"
                "   SlidingFric 2.700000\n"
                " }\n"
                " WheelBack {\n"
                "   SuspensionExtent 0.200000\n"
                "   SuspensionLimit 0.100000\n"
                "   SuspensionFactor 1.300000\n"
                "   SuspensionDampCoef 0.030000\n"
                "   SteeringLimit 0.000000\n"
                "   SteeringOffset 0.000000\n"
                "   BrakeCoef 0.400000\n"
                "   HandbrakeCoef 2.000000\n"
                "   CamberLimit -1.000000\n"
                "   WobbleLimit 0.000000\n"
                "   TireDispLimitLong 0.125000\n"
                "   TireDampCoefLong 0.250000\n"
                "   TireDragCoefLong 0.020000\n"
                "   TireDispLimitLat 0.125000\n"
                "   TireDampCoefLat 0.250000\n"
                "   TireDragCoefLat 0.050000\n"
                "   OptimumSlipPercent 0.057000\n"
                "   StaticFric 3.000000\n"
                "   SlidingFric 1.400000\n"
                " }\n"
                " AxleFront {\n"
                "   TorqueCoef 1.000000\n" 
                "   DampCoef 0.500000\n"
                " }\n"
                " AxleBack {\n"
                "   TorqueCoef 1.000000\n"
                "   DampCoef 0.500000\n"
                " }\n"
            "}\n"
            )
            with open(veh_carsim_file_path, "w") as file:
                file.write(content)
            return veh_carsim_file_path
        
        # # tune\vehicle\ .vehGyro
        def generate_veh_gyro_file():
            veh_gyro_file_path = os.path.join(vehicle_folder_path, f"{vehicle_name}.vehGyro")
            content = (
                "type: a\n"
                "vehGyro {\n"
                "   Drift 0.200000\n"
                "   Spin180 0.850000\n"
                "   Reverse180 4.000002\n" 
                "   Pitch 0.000000\n"
                "   Roll 0.000000\n"
                "}\n"
            )
            with open(veh_gyro_file_path, "w") as file:
                file.write(content)
            return veh_gyro_file_path
        
        # # tune\vehicle\ .vehStuck
        def generate_veh_stuck_file():
            veh_stuck_file_path = os.path.join(vehicle_folder_path, f"{vehicle_name}.vehStuck")
            content = (
                "type: a\n"
                "vehStuck {\n"
                "   Turn 3.141593 \n"
                "   Rotation 0.000000\n"
                "   Translation 0.100000\n" 
                "   TimeThresh 1.000000\n" 
                "   PosThresh 1.250000\n"
                "   MoveThresh 1.750000\n" 
                " }\n"
            )
            with open(veh_stuck_file_path, "w") as file:
                file.write(content)
            return veh_stuck_file_path
        
        # # tune\vehicle\ _opp.vehCarSim
        def generate_veh_opp_carsim_file():
            veh_opp_carsim_file_path = os.path.join(vehicle_folder_path, f"{vehicle_name}_opp.vehCarSim")
            content = (
                "type: a\n"
                "vehCarSim {\n"
                "   Mass 1300.000000\n"
                "   InertiaBox 4.500000   1.600000    4.000000\n"
                "   CenterOfGravity 0.000000  -0.350000   0.300000\n"
                "   BoundFriction 0.200000\n"
                "   BoundElasticity 0.300000\n"
                "   DrivetrainType 0\n"
                "   SSSValue 1.000000\n"
                "   SSSThreshold 0.000000\n"
                "   CarFrictionHandling 1.000000\n"
                "   Aero {\n"
                        "AngCDamp 0.000000   7.030000    1.000000\n"
                        "AngVelDamp 0.000000 0.000000    0.000000\n"
                        "AngVel2Damp 0.000000    2.340000    2.000000\n"
                        "Drag 0.000000\n"
                        "Down 0.000000\n"
                " }\n"
                "   Engine {\n"
                    "   AngInertia 1.000000 \n"
                    "   MaxHorsePower 450.000000 \n"
                    "   OptRPM 8000.000000 \n"
                    "   MaxRPM 8500.000000 \n"
                    "   GCL 0.250000 \n"
                " }\n"
                "   Trans {\n"
                    "   NumGears 7 \n"
                    "   GearRatios -20.000000 0.000000 28.000000 20.000000 16.000000 12.000000 6.500000 0.000000 \n"
                    "   UpshiftRPM 6000.000000 7500.000000 7700.000000 7600.000000 7500.000000 7500.000000 7500.000000 7500.000000 \n"
                    "   DownshiftRPM 3000.000000 3000.000000 2500.000000 2500.000000 2500.000000 2500.000000 2000.000000 2000.000000 \n"
                    "   ManualNumGears 7 \n"
                    "   ManualGearRatios -20.000000 0.000000 28.000000 20.000000 16.000000 12.000000 6.499999 0.000000 \n"
                    "   DownshiftBias 1.850000 \n"
                " }\n"
                "   Drivetrain {\n"
                    "   AngInertia 2000.000000 \n"
                    "   BrakeDynamicCoef 1.000000 \n"
                    "   BrakeStaticCoef 1.200000 \n"
                " }\n"
                "   Freetrain {\n"
                    "   AngInertia 2000.000000 \n"
                    "   BrakeDynamicCoef 1.000000 \n"
                    "   BrakeStaticCoef 1.200000 \n"
                " }\n"
                "   WheelFront {\n"
                    "   SuspensionExtent 0.200000 \n"
                    "   SuspensionLimit 0.100000 \n"
                    "   SuspensionFactor 1.000000 \n"
                    "   SuspensionDampCoef 0.100000 \n"
                    "   SteeringLimit 0.500000 \n"
                    "   SteeringOffset 0.250000 \n"
                    "   BrakeCoef 0.132000 \n"
                    "   CamberLimit 0.409000 \n"
                    "   TireDispLimitLong 0.075000 \n"
                    "   TireDampCoefLong 0.750000 \n"
                    "   TireDispLimitLat 0.075000 \n"
                    "   TireDampCoefLat 0.750000 \n"
                    "   OptimumSlipPercent 0.140000 \n"
                    "   StaticFric 3.000000 \n"
                    "   SlidingFric 3.000000 \n"
                " }\n"
                "   WheelBack {\n"
                    "   SuspensionExtent 0.200000 \n"
                    "   SuspensionLimit 0.100000 \n"
                    "   SuspensionFactor 1.000000 \n"
                    "   SuspensionDampCoef 0.100000 \n"
                    "   SteeringLimit 0.040000 \n"
                    "   SteeringOffset 0.000000 \n"
                    "   BrakeCoef 0.500000 \n"
                    "   CamberLimit 0.170605 \n"
                    "   TireDispLimitLong 0.055000 \n"
                    "   TireDampCoefLong 0.750000 \n"
                    "   TireDispLimitLat 0.055000 \n"
                    "   TireDampCoefLat 0.750000 \n"
                    "   OptimumSlipPercent 0.140000 \n"
                    "   StaticFric 2.000000 \n"
                    "   SlidingFric 1.700000 \n"
                " }\n"
                "   AxleFront {\n"
                    "   TorqueCoef 0.000000 \n"
                    "   DampCoef 0.000000 \n"
                " }\n"
                "   AxleBack {\n"
                    "   TorqueCoef 0.000000 \n"
                    "   DampCoef 0.000000 \n"
                " }\n"
            "   }\n"
            )
            with open(veh_opp_carsim_file_path, "w") as file:
                file.write(content)
            return veh_opp_carsim_file_path
        
        # tune\vehicle\camera _near.camTrackCS
        def generate_near_camTrackCS_file():
            near_camTrackCS_file_path = os.path.join(camera_folder_path, f"{vehicle_name}_near.camTrackCS")
            content = (
                "type: a\n"
                "camTrackCS {\n"
                    "  Offset 0.000000 1.510000 5.390000\n"
                    "   CollideType 1\n"
                    "   MinMaxOn 1\n"
                    "   TrackBreak 1\n"
                    "   MinAppXZPos 1.600000\n"
                    "   MaxAppXZPos 29.200001\n"
                    "   MinSpeed 0.000000\n"
                    "   MaxSpeed 12.300000\n"
                    "   AppInc 3.900000\n"
                    "   AppDec 10.000000\n"
                    "   MinHardSteer 0.800000\n"
                    "   DriftDelay 0.300000\n"
                    "   VertOffset 1.000000\n"
                    "   FrontRate 0.550000\n"
                    "   RearRate 0.500000\n"
                    "   FlipDelay 0.500000\n"
                    "   SteerOn 0\n"
                    "   SteerMin 0.500000\n"
                    "   SteerAmt 3.500000\n"
                    "   HillMin -0.713000\n"
                    "   HillMax 0.466000\n"
                    "   HillLerp 0.354000\n"
                    "   ApproachOn 1\n"
                    "   AppAppOn 1\n"
                    "   AppRot 60.000000\n"
                    "   AppXRot 6.970000\n"
                    "   AppYPos 4.819998\n"
                    "   AppXZPos 28.052279\n"
                    "   AppApp 0.700000\n"
                    "   AppRotMin 0.010000\n"
                    "   AppPosMin 0.250000\n"
                    "   LookAbove 0.710000\n"
                    "   TrackTo 0.000000 1.551000 0.000000\n"
                    "   MaxDist 6.150000\n"
                    "   MinDist 1.000000\n"
                    "   LookAt 1.000000\n"
                    "   BlendTime 1.200000\n"
                    "   BlendGoal 1.000000\n"
                    "   CameraFOV 70.000000\n"
                    "   CameraNear 0.500000\n"
                    "   CameraFar 150.909058\n"
                "}\n"
            )
            with open(near_camTrackCS_file_path, "w") as file:
                file.write(content)
            return near_camTrackCS_file_path
        
        # tune\vehicle\camera _dash.camPovCS
        def generate_dash_camPovCS_file():
            dash_camPovCS_file_path = os.path.join(camera_folder_path, f"{vehicle_name}_dash.camPovCS")
            content = (
                "type: a\n"
                "camPovCS {\n"
                "    Offset 0.000000 1.101900 -0.127200\n"
                "    ReverseOffset 0.000000 1.700000 0.750000\n"
                "    Pitch 0.000000\n"
                "    POVJitterAmp 0.000000\n"
                "    ApproachOn 1\n"
                "    AppAppOn 1\n"
                "    AppRot 28.000000\n"
                "    AppXRot 7.860001\n"
                "    AppYPos 33.340000\n"
                "    AppXZPos 28.000000\n"
                "    AppApp 0.700000\n"
                "    AppRotMin 0.000000\n"
                "    AppPosMin 0.000000\n"
                "    LookAbove -1.000000\n"
                "    TrackTo 0.000000 1.619000 0.000000\n"
                "    MaxDist 0.000000\n"
                "    MinDist 0.000000\n"
                "    LookAt 0.000000\n"
                "    BlendTime 1.200000\n"
                "    BlendGoal 1.000000\n"
                "    CameraFOV 70.000000\n"
                "    CameraNear 0.100000\n"
                "    CameraFar 600.000000\n"
                " }\n"
            )
            with open(dash_camPovCS_file_path, "w") as file:
                file.write(content)
            return dash_camPovCS_file_path
        
        # tune\vehicle\camera .camPovCS
        def generate_camPovCS_file():
            camPovCS_file_path = os.path.join(camera_folder_path, f"{vehicle_name}.camPovCS")
            content = (
                "type: a\n"
                "camPovCS {\n"
                "   Offset 0.000000 1.101900 -0.127200\n"
                "   Pitch 0.000000\n"
                "   POVJitterAmp 0.000000\n"
                "   ApproachOn 1\n"
                "   AppAppOn 1\n"
                "   AppRot 28.000000\n"
                "   AppXRot 7.860001\n"
                "   AppYPos 33.340000\n"
                "   AppXZPos 28.000000\n"
                "   AppApp 0.700000\n"
                "   AppRotMin 0.000000\n"
                "   AppPosMin 0.000000\n"
                "   LookAbove -1.000000\n"
                "   TrackTo 0.000000 1.619000 0.000000\n"
                "   MaxDist 0.000000\n"
                "   MinDist 0.000000\n"
                "   LookAt 0.000000\n"
                "   BlendTime 1.200000\n"
                "   BlendGoal 1.000000\n"
                "   CameraFOV 69.999954\n"
                "   CameraNear 0.100000\n"
                "   CameraFar 364.545410\n"
                "}\n"
            )
            with open (camPovCS_file_path, "w") as file:
                file.write(content)
            return camPovCS_file_path
        
        # tune\vehicle\camera\ _far.camTrackCS
        def generate_far_camTrackCS_file():
            far_camTrackCS_file_path = os.path.join(camera_folder_path, f"{vehicle_name}_far.camTrackCS")
            content = (
                "type: a"
                "camTrackCS {"
                "   Offset 0.000000 2.200000 6.900000\n"
                "   CollideType 1\n"
                "   MinMaxOn 1\n"
                "   TrackBreak 1\n"
                "   MinAppXZPos 0.800000\n"
                "   MaxAppXZPos 10.000004\n"
                "   MinSpeed 0.000000\n"
                "   MaxSpeed 12.150004\n"
                "   AppInc 3.499999\n"
                "   AppDec 10.000003\n"
                "   MinHardSteer 0.800000\n"
                "   DriftDelay 0.300000\n"
                "   VertOffset 1.000000\n"
                "   FrontRate 0.550000\n"
                "   RearRate 0.500000\n"
                "   FlipDelay 0.500000\n"
                "   SteerOn 0\n"
                "   SteerMin 0.500000\n"
                "   SteerAmt 3.500000\n"
                "   HillMin -0.713000\n"
                "   HillMax 0.466000\n"
                "   HillLerp 0.152000\n"
                "   ReverseOn 1\n"
                "   RevDelay 2.000000\n"
                "   RevOnApp 2.000000\n"
                "   RevOffApp 4.000000\n"
                "   ApproachOn 1\n"
                "   AppAppOn 1\n"
                "   AppRot 60.000000\n"
                "   AppXRot 3.000000\n"
                "   AppYPos 10.080002\n"
                "   AppXZPos 0.800000\n"
                "   AppApp 0.700000\n"
                "   AppRotMin 0.010000\n"
                "   AppPosMin 0.250000\n"
                "   LookAbove 1.400000\n"
                "   TrackTo 0.000000 0.800000 0.000000\n"
                "   MaxDist 7.850000\n"
                "   MinDist 6.100001\n"
                "   LookAt 1.000000\n"
                "   BlendTime 1.200000\n"
                "   BlendGoal 1.000000\n"
                "   CameraFOV 70.000000\n"
                "   CameraNear 0.500000\n"
                "   CameraFar 600.000000\n"
                "}\n"
            )
            with open(far_camTrackCS_file_path, "w") as file:
                file.write(content)
            return far_camTrackCS_file_path
        
        # tune\banger\ _HEADLIGHT1.dgBangerData
        def generate_HEADLIGHT1_dgBangerData_file():
            HEADLIGHT1_dgBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_HEADLIGHT1.dgBangerData")
            content = (
                "type: a\n"
                "dgBangerData {\n"
                "   AudioId 0\n"
                "    Size 0.500000 0.500000    0.100000\n"
                "    CG 0.000000   0.000000    -0.000000\n" 
                "    NumGlows 0 \n"
                "    Mass 19.999998 \n"
                "    Elasticity 0.500000\n"
                "    Friction 0.900000\n"
                "    ImpulseLimit2 624.999939\n"
                "    SpinAxis 0\n"
                "    Flash 0\n"
                "    NumParts 0\n"
                "    BirthRule {\n"
                "        Position 0.000000   0.000000    0.000000\n" 
                "        PositionVar 0.000000    0.000000    0.000000\n"
                "        Velocity 0.000000   0.000000    0.000000\n"
                "        VelocityVar 0.000000    0.000000    0.000000\n"
                "        Life 1.000000\n"
                "        Mass 1.000000\n"
                "        MassVar 0.000000\n"
                "        Radius 1.000000\n"
                "        RadiusVar 0.000000\n"
                "        Drag 0.000000\n"
                "        DragVar 0.000000\n"
                "        DRadius 0.000000\n"
                "        DRadiusVar 0.000000\n"
                "        DAlpha 0\n"
                "        DAlphaVar 0\n"
                "        DRotation 0\n"
                "        DRotationVar 0\n"
                "        InitialBlast 0\n"
                "        SpewRate 0.000000\n"
                "        SpewTimeLimit 0.000000\n"
                "        Gravity -9.800000\n"
                "        TexFrameStart 0\n"
                "        TexFrameEnd 0\n"
                "        BirthFlags 0\n"
                "   }\n"
                "    TexNumber 0\n"
                "    BillFlags 0\n"
                "    YRadius 0.000000\n"
                "    ColliderId 0\n"
                "    CollisionPrim 1\n"
                "    CollisionType 16\n"
                "}\n"
            )
            with open (HEADLIGHT1_dgBangerData_file_path, "w") as file:
                file.write(content)
            return HEADLIGHT1_dgBangerData_file_path
        
        # tune\banger\ _HEADLIGHT0.dgBangerData
        def generate_HEADLIGHT0_dgBangerData_file():
            HEADLIGHT0_dgBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_HEADLIGHT0.dgBangerData")
            content = (
                "type: a\n"
                "dgBangerData {\n"
                "   AudioId 0\n"
                "    Size 0.500000 0.500000    0.100000\n"
                "    CG 0.000000   0.000000    -0.000000\n" 
                "    NumGlows 0 \n"
                "    Mass 19.999998 \n"
                "    Elasticity 0.500000\n"
                "    Friction 0.900000\n"
                "    ImpulseLimit2 624.999939\n"
                "    SpinAxis 0\n"
                "    Flash 0\n"
                "    NumParts 0\n"
                "    BirthRule {\n"
                "        Position 0.000000   0.000000    0.000000\n" 
                "        PositionVar 0.000000    0.000000    0.000000\n"
                "        Velocity 0.000000   0.000000    0.000000\n"
                "        VelocityVar 0.000000    0.000000    0.000000\n"
                "        Life 1.000000\n"
                "        Mass 1.000000\n"
                "        MassVar 0.000000\n"
                "        Radius 1.000000\n"
                "        RadiusVar 0.000000\n"
                "        Drag 0.000000\n"
                "        DragVar 0.000000\n"
                "        DRadius 0.000000\n"
                "        DRadiusVar 0.000000\n"
                "        DAlpha 0\n"
                "        DAlphaVar 0\n"
                "        DRotation 0\n"
                "        DRotationVar 0\n"
                "        InitialBlast 0\n"
                "        SpewRate 0.000000\n"
                "        SpewTimeLimit 0.000000\n"
                "        Gravity -9.800000\n"
                "        TexFrameStart 0\n"
                "        TexFrameEnd 0\n"
                "        BirthFlags 0\n"
                "   }\n"
                "    TexNumber 0\n"
                "    BillFlags 0\n"
                "    YRadius 0.000000\n"
                "    ColliderId 0\n"
                "    CollisionPrim 1\n"
                "    CollisionType 16\n"
                " }\n"
            )
            with open (HEADLIGHT0_dgBangerData_file_path, "w") as file:
                file.write(content)
            return HEADLIGHT0_dgBangerData_file_path
        
        # \tune\banger\ _WHL1.dgBangerData
        def generate_WHL1_dgBangerData_file():
            WHL1_dbBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_WHL1.dbBangerData")
            content = (
                "type: a\n"
                "dgBangerData {\n"
                "   AudioId 0\n"
                "   Size 0.255432 0.694702    0.694702\n"
                "   CG 0.000000   0.000000    0.000000\n"
                "   NumGlows 0\n"
                "   Mass 98.619286\n"
                "   Elasticity 0.500000\n"
                "   Friction 0.900000\n"
                "   ImpulseLimit2 3081.852539\n"
                "   SpinAxis 0\n"
                "   Flash 0\n"
                "   NumParts 0\n"
                "   BirthRule {\n"
                "       Position 0.000000   0.000000    0.000000 \n"
                "       PositionVar 0.000000    0.000000    0.000000 \n"
                "       Velocity 0.000000   0.000000    0.000000 \n"
                "       VelocityVar 0.000000    0.000000    0.000000 \n"
                "       Life 1.000000 \n"
                "       Mass 1.000000 \n"
                "       MassVar 0.000000 \n"
                "       Radius 1.000000 \n"
                "       RadiusVar 0.000000 \n"
                "       Drag 0.000000 \n"
                "       DragVar 0.000000 \n"
                "       DRadius 0.000000 \n"
                "       DRadiusVar 0.000000 \n"
                "       DAlpha 0 \n"
                "       DAlphaVar 0 \n"
                "       DRotation 0 \n"
                "       DRotationVar 0 \n"
                "       InitialBlast 0 \n"
                "       SpewRate 0.000000 \n"
                "       SpewTimeLimit 0.000000 \n"
                "       Gravity -9.800000 \n"
                "       TexFrameStart 0 \n"
                "       TexFrameEnd 0 \n"
                "       BirthFlags 0 \n"
                "   }\n"
                "   TexNumber 0\n"
                "   BillFlags 0\n"
                "   YRadius 0.000000\n"
                "   ColliderId 0\n"
                "   CollisionPrim 1\n"
                "   CollisionType 16\n"
                "}\n"
            )
            with open (WHL1_dbBangerData_file_path, "w") as file:
                file.write(content)
            return WHL1_dbBangerData_file_path
        
        # tune\banger\ _WHL0.dbBangerData
        def generate_WHL0_dgBangerData_file():
            WHL0_dgBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_WHL0.dgBangerData")
            content = (
                "type: a\n"
                "dgBangerData {\n"
                "   AudioId 0\n"
                "   Size 0.257615 0.694702    0.694702\n"
                "   CG 0.000000   0.000000    -0.000000\n"
                "   NumGlows 0\n"
                "   Mass 99.462181\n"
                "   Elasticity 0.500000\n"
                "   Friction 0.900000\n"
                "   ImpulseLimit2 3108.193115\n"
                "   SpinAxis 0\n"
                "   Flash 0\n"
                "   NumParts 0\n"
                "   BirthRule {\n"
                "   Position 0.000000   0.000000    0.000000\n"
                "   PositionVar 0.000000    0.000000    0.000000\n"
                "   Velocity 0.000000   0.000000    0.000000\n"
                "   VelocityVar 0.000000    0.000000    0.000000\n"
                "   Life 1.000000\n"
                "   Mass 1.000000\n"
                "   MassVar 0.000000\n"
                "   Radius 1.000000\n"
                "   RadiusVar 0.000000\n"
                "   Drag 0.000000\n"
                "   DragVar 0.000000\n"
                "   DRadius 0.000000\n"
                "   DRadiusVar 0.000000\n"
                "   DAlpha 0\n"
                "   DAlphaVar 0\n"
                "   DRotation 0\n"
                "   DRotationVar 0\n"
                "   InitialBlast 0\n"
                "   SpewRate 0.000000\n"
                "   SpewTimeLimit 0.000000\n"
                "   Gravity -9.800000\n"
                "   TexFrameStart 0\n"
                "   TexFrameEnd 0\n"
                "   BirthFlags 0\n"
                " }\n"
                " TexNumber 0\n"
                " BillFlags 0\n"
                " YRadius 0.000000\n"
                " ColliderId 0\n"
                " CollisionPrim 1\n"
                " CollisionType 16\n"
                "}\n"
            )
            with open(WHL0_dgBangerData_file_path, "w") as file:
                file.write(content)
            return WHL0_dgBangerData_file_path
        
        # tune\banger\ _WHL2.dgBangerData
        def generate_WHL2_dgBangerData_file():
            WHL2_dgBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_WHL2.dgBangerData")
            content = (
            "type: a\n"
            "dgBangerData {\n"
            "      AudioId 0 \n"
            "      Size 0.333296 0.729726    0.729726 \n"
            "      CG -0.000000  -0.000000   0.000000 \n"
            "      NumGlows 0 \n"
            "      Mass 141.984161 \n"
            "      Elasticity 0.500000 \n"
            "      Friction 0.900000 \n"
            "      ImpulseLimit2 4437.004883 \n"
            "      SpinAxis 0 \n"
            "      Flash 0 \n"
            "      NumParts 0 \n"
            "      BirthRule {\n"
            "        Position 0.000000   0.000000    0.000000 \n"
            "        PositionVar 0.000000    0.000000    0.000000\n" 
            "        Velocity 0.000000   0.000000    0.000000 \n"
            "        VelocityVar 0.000000    0.000000    0.000000\n" 
            "        Life 1.000000 \n"
            "        Mass 1.000000 \n"
            "        MassVar 0.000000 \n"
            "        Radius 1.000000 \n"
            "        RadiusVar 0.000000 \n"
            "        Drag 0.000000 \n"
            "        DragVar 0.000000 \n"
            "        DRadius 0.000000 \n"
            "        DRadiusVar 0.000000 \n"
            "        DAlpha 0 \n"
            "        DAlphaVar 0 \n"
            "        DRotation 0 \n"
            "        DRotationVar 0 \n"
            "        InitialBlast 0 \n"
            "        SpewRate 0.000000 \n"
            "        SpewTimeLimit 0.000000 \n"
            "        Gravity -9.800000 \n"
            "        TexFrameStart 0 \n"
            "        TexFrameEnd 0 \n"
            "        BirthFlags 0 \n"
            "        }\n"
            "      TexNumber 0 \n"
            "      BillFlags 0 \n"
            "      YRadius 0.000000 \n"
            "      ColliderId 0 \n"
            "      CollisionPrim 1 \n"
            "      CollisionType 16 \n"
            "}\n"
            )
            with open(WHL2_dgBangerData_file_path, "w") as file:
                file.write(content)
            return WHL2_dgBangerData_file_path
        
        # tune\banger\ _WHL3.dgBangerData
        def generate_WHL3_dgBangerData_file():
            WHL3_dgBangerData_file_path = os.path.join(banger_folder_path, f"{vehicle_name}_WHL3.dgBangerData")
            content = (
            "type: a\n"
            "dgBangerData {\n"
            "   AudioId 0 \n"
            "   Size 0.333296 0.729726    0.729726 \n"
            "   CG 0.000000   0.000000    0.000000 \n"
            "   NumGlows 0 \n"
            "   Mass 141.984146 \n"
            "   Elasticity 0.500000 \n"
            "   Friction 0.900000 \n"
            "   ImpulseLimit2 4437.004883 \n"
            "   SpinAxis 0 \n"
            "   Flash 0 \n"
            "   NumParts 0 \n"
            "   BirthRule {\n"
            "        Position 0.000000   0.000000    0.000000 \n"
            "        PositionVar 0.000000    0.000000    0.000000 \n"
            "        Velocity 0.000000   0.000000    0.000000 \n"
            "        VelocityVar 0.000000    0.000000    0.000000 \n"
            "        Life 1.000000 \n"
            "        Mass 1.000000 \n"
            "        MassVar 0.000000 \n"
            "        Radius 1.000000 \n"
            "        RadiusVar 0.000000 \n"
            "        Drag 0.000000 \n"
            "        DragVar 0.000000 \n"
            "        DRadius 0.000000 \n"
            "        DRadiusVar 0.000000 \n"
            "        DAlpha 0 \n"
            "        DAlphaVar 0 \n"
            "        DRotation 0 \n"
            "        DRotationVar 0 \n"
            "        InitialBlast 0 \n"
            "        SpewRate 0.000000 \n"
            "        SpewTimeLimit 0.000000 \n"
            "        Gravity -9.800000 \n"
            "        TexFrameStart 0 \n"
            "        TexFrameEnd 0 \n"
            "        BirthFlags 0 \n"
            "        }\n"
            "  TexNumber 0 \n"
            "  BillFlags 0 \n"
            "  YRadius 0.000000 \n"
            "  ColliderId 0 \n"
            "  CollisionPrim 1 \n"
            "  CollisionType 16 \n"
            "}\n"
            )
            with open(WHL3_dgBangerData_file_path, "w") as file:
                file.write(content)
            return WHL3_dgBangerData_file_path

        # Function to write CSV files (moved out of generate_aud_cardata_files)
        def write_csv(file_path, data):
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    for row in data:
                        writer.writerow(row)
                return file_path
            except Exception as e:
                raise Exception(f"Error writing CSV file '{file_path}': {e}")

        # \aud\cardata\opponent and \player
        def generate_aud_cardata_files(base_path, vehicle_name):
            opponent_file_path = os.path.join(base_path, "aud", "cardata", "opponent", f"{vehicle_name}.csv")
            player_file_path = os.path.join(base_path, "aud", "cardata", "player", f"{vehicle_name}.csv")


            opponent_data = [
                ["Horn wave name", "Horn volume", "flags", "Num Engine Samples", "clutch wave name", "clutch volume"],
                [f"{vehicle_name}HORN", 0.95, 0, 2, "REVERSE", 0.93],
                [
                    "Engine wave name", "Min Volume", "Max Volume", "fade in start RPM", "fade in end RPM",
                    "fade out start RPM", "fade out end RPM", "Min Pitch", "Max Pitch", "Pitch shift start RPM", "Pitch shift end RPM"
                ],
                [f"{vehicle_name}LOW", 0.91, 0.94, 500, 2500, 7000, 10500, 0.65, 3.0, 500, 14000],
            ]

            player_data = [
                ["Horn wave name", "Horn volume", "flags", "Num Engine Samples", "clutch wave name", "clutch volume"],
                [f"{vehicle_name}HORN", 0.95, 0, 2, "REVERSE", 0.93],
                [
                    "Engine wave name", "Min Volume", "Max Volume", "fade in start RPM", "fade in end RPM",
                    "fade out start RPM", "fade out end RPM", "Min Pitch", "Max Pitch", "Pitch shift start RPM", "Pitch shift end RPM"
                ],
                [f"{vehicle_name}IDLE", 0.82, 0.87, 1.0, 500, 2500, 7000, 0.95, 2.0, 1.0, 4000],
                [f"{vehicle_name}LOW", 0.672, 0.8928, 500, 1500, 7000, 10500, 0.8, 2.5, 500, 12000],
                [f"{vehicle_name}MID", 0.528, 0.912, 1000, 4000, 5000, 10000, 0.5, 1.5, 200, 5500],
                [f"{vehicle_name}HIGH", 0.672, 0.952, 1000, 7500, 15000, 15000, 0.65, 1.75, 2000, 11000],
            ]

            return opponent_file_path, player_file_path, opponent_data, player_data


        def write_csv(file_path, data):
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                print(f"Writing CSV to: {file_path}")
                with open(file_path, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    for row in data:
                        writer.writerow(row)
                print(f"Successfully written: {file_path}")
                return file_path
            except Exception as e:
                raise Exception(f"Error writing CSV file '{file_path}': {e}")
        
        # Generate files and write CSV data
        try:
            # Generate configuration files
            info_file_path = generate_info_file()
            asnode_file_path = generate_asnode_file()
            mm_mirror_file_path = generate_mm_mirror_file()
            dash_asnode_file_path = generate_dash_asnode_file()
            veh_cardamage_file_path = generate_veh_cardamage_file()
            veh_carsim_file_path = generate_veh_carsim_file()
            veh_gyro_file_path = generate_veh_gyro_file()
            veh_stuck_file_path = generate_veh_stuck_file()
            veh_opp_carsim_file_path = generate_veh_opp_carsim_file()
            near_camTrackCS_file_path = generate_near_camTrackCS_file()
            dash_camPovCS_file_path = generate_dash_camPovCS_file()
            camPovCS_file_path = generate_camPovCS_file()
            far_camTrackCS_file_path = generate_far_camTrackCS_file()
            HEADLIGHT1_dgBangerData_file_path = generate_HEADLIGHT1_dgBangerData_file()
            HEADLIGHT0_dgBangerData_file_path = generate_HEADLIGHT0_dgBangerData_file()
            WHL1_dgBangerData_file_path = generate_WHL1_dgBangerData_file()
            WHL0_dgBangerData_file_path = generate_WHL0_dgBangerData_file()
            WHL2_dgBangerData_file_path = generate_WHL2_dgBangerData_file()
            WHL3_dgBangerData_file_path = generate_WHL3_dgBangerData_file()
            opponent_file_path, player_file_path, opponent_data, player_data = generate_aud_cardata_files(base_path, vehicle_name)
            opponent_csv = write_csv(opponent_file_path, opponent_data)
            player_csv = write_csv(player_file_path, player_data)

        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create configuration files or CSV files: {e}")
            return

        # Show success message
        QMessageBox.information(
            self,
            "Success",
            f"Folder structure and configuration files created successfully!\n\n"
            f"Base Path: {base_path}\n"
            f"Tune Info File: {info_file_path}\n"
            f"Tune asNode File: {asnode_file_path}\n"
            f"Tune mmMirror File: {mm_mirror_file_path}\n"
            f"Tune Dash asNode File: {dash_asnode_file_path}\n"
            f"Vehicle Damage File: {veh_cardamage_file_path}\n"
            f"Vehicle Carsim File: {veh_carsim_file_path}\n"
            f"Vehicle Gyro File: {veh_gyro_file_path}\n"
            f"Vehicle Stuck File: {veh_stuck_file_path}\n"
            f"Vehicle Opp Carsim File: {veh_opp_carsim_file_path}\n"
            f"Camera near camTrackCS File: {near_camTrackCS_file_path}\n"
            f"Camera dash camPovCS File: {dash_camPovCS_file_path}\n"
            f"Camera camPovCS File: {camPovCS_file_path}\n"
            f"Camera far camTrackCS File: {far_camTrackCS_file_path}\n"
            f"Banger HEADLIGHT1 File: {HEADLIGHT1_dgBangerData_file_path}\n"
            f"Banger HEADLIGHT0 File: {HEADLIGHT0_dgBangerData_file_path}\n"
            f"Banger WHL1 File: {WHL1_dgBangerData_file_path}\n"
            f"Banger WHL0 File: {WHL0_dgBangerData_file_path}\n"
            f"Banger WHL2 File: {WHL2_dgBangerData_file_path}\n"
            f"Banger WHL3 File: {WHL3_dgBangerData_file_path}\n"
            f"Cardata Opponent CSV: {opponent_csv}\n"
            f"Cardata Player CSV: {player_csv}\n"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set application metadata
    app.setApplicationName("MM2 Structure Generator")
    app.setOrganizationName("Chassey Blue")
    app.setOrganizationDomain("https://chasseyblue.com")
    window = VehicleFolderSetup()
    window.show()
    sys.exit(app.exec_())
