# frozen_string_literal: true

# Appendix G Baseline Generation Measure
#
# Generate ASHRAE 90.1 Appendix G baseline model from proposed design.
# Implements all required baseline transformations per code requirements.
#
# Usage:
#   Apply this measure in OpenStudio Application or via CLI
#
# TODO: Implement Appendix G baseline generation logic

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

# start the measure
class AppendixGBaseline < OpenStudio::Measure::ModelMeasure
  # human readable name
  def name
    return 'Appendix G Baseline Generation'
  end

  # human readable description
  def description
    return 'Generate ASHRAE 90.1 Appendix G baseline model with all required transformations for LEED compliance'
  end

  # human readable description of modeling approach
  def modeler_description
    return 'TODO: Implement ASHRAE 90.1 Appendix G baseline transformations including envelope, lighting, HVAC, and service hot water'
  end

  # define the arguments that the user will input
  def arguments(model)
    args = OpenStudio::Measure::OSArgumentVector.new

    # TODO: Add arguments for:
    # - Climate zone
    # - Building type
    # - ASHRAE 90.1 version (2019, 2022, etc.)

    return args
  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)

    # TODO: Implement measure logic per ASHRAE 90.1 Appendix G
    # 1. Transform envelope to baseline constructions
    # 2. Adjust window-to-wall ratio per Appendix G rules
    # 3. Apply baseline lighting power densities
    # 4. Replace HVAC systems with baseline system types
    # 5. Set baseline efficiencies per equipment tables
    # 6. Apply economizer requirements per climate zone
    # 7. Set service hot water to 50% of proposed
    # 8. Generate report of all transformations

    runner.registerInfo('TODO: Implement Appendix G baseline generation measure')

    return true
  end
end

# register the measure to be used by the application
AppendixGBaseline.new.registerWithApplication
