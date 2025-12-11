# frozen_string_literal: true

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'

class YourMeasureNameTest < Minitest::Test
  # Method to load an example model for testing
  # Option 1: Load from an existing OSM file
  def load_test_model(osm_path = nil)
    if osm_path.nil?
      # Create a simple test model programmatically
      model = OpenStudio::Model::Model.new

      # Add basic building geometry
      # Example: Single space with one thermal zone
      space = OpenStudio::Model::Space.new(model)
      space.setName('Test Space')

      zone = OpenStudio::Model::ThermalZone.new(model)
      zone.setName('Test Zone')
      space.setThermalZone(zone)

      return model
    else
      # Load from file
      translator = OpenStudio::OSVersion::VersionTranslator.new
      path = OpenStudio::Path.new(osm_path)
      model = translator.loadModel(path)
      assert(model.is_initialized, "Could not load model from #{osm_path}")
      return model.get
    end
  end

  # Test that the measure has the correct number of arguments
  def test_number_of_arguments_and_argument_names
    # Create an instance of the measure
    measure = YourMeasureName.new

    # Create an empty model
    model = OpenStudio::Model::Model.new

    # Get arguments and test that they are what we expect
    arguments = measure.arguments(model)
    assert_equal(0, arguments.size) # Update this based on your measure's arguments

    # If you have arguments, test their names
    # assert_equal('example_argument', arguments[0].name)
  end

  # Test running the measure with default arguments
  def test_run_with_defaults
    # Create an instance of the measure
    measure = YourMeasureName.new

    # Create a test model
    model = load_test_model

    # Create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    # Get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # Run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # Show the output
    show_output(result)

    # Assert that it ran successfully
    assert_equal('Success', result.value.valueName)

    # Check for expected info, warning, or error messages
    # assert(result.info.size > 0)
    # assert_equal(0, result.warnings.size)
    # assert_equal(0, result.errors.size)
  end

  # Test running the measure with specific argument values
  def test_run_with_custom_arguments
    # Create an instance of the measure
    measure = YourMeasureName.new

    # Create a test model
    model = load_test_model

    # Create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    # Get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # Set custom argument values
    # example_double = arguments[0].clone
    # assert(example_double.setValue(15.0))
    # argument_map['example_double'] = example_double

    # Run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # Show the output
    show_output(result)

    # Assert that it ran successfully
    assert_equal('Success', result.value.valueName)

    # Add specific assertions about what changed in the model
    # assert_equal(expected_value, actual_value, 'Error message if assertion fails')
  end

  # Test that the measure handles invalid arguments appropriately
  def test_invalid_argument_values
    # Create an instance of the measure
    measure = YourMeasureName.new

    # Create a test model
    model = load_test_model

    # Create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    # Get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # Set an invalid argument value
    # example_double = arguments[0].clone
    # assert(example_double.setValue(-10.0))  # Invalid if must be positive
    # argument_map['example_double'] = example_double

    # Run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # Show the output
    show_output(result)

    # Assert that it failed as expected
    # assert_equal('Fail', result.value.valueName)
    # assert(result.errors.size > 0)
  end

  # Test that the measure registers as "Not Applicable" when appropriate
  def test_not_applicable
    # Create an instance of the measure
    measure = YourMeasureName.new

    # Create a model that doesn't have the objects needed for this measure
    model = OpenStudio::Model::Model.new

    # Create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    # Get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # Run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # Show the output
    show_output(result)

    # Assert that it registered as not applicable
    # assert_equal('NA', result.value.valueName)
  end

  # Test with a real building model (if you have a test OSM file)
  def test_with_example_model
    # Skip this test if example model doesn't exist
    osm_path = File.expand_path('../tests/example_model.osm', __dir__)
    skip('Example model not found') unless File.exist?(osm_path)

    # Create an instance of the measure
    measure = YourMeasureName.new

    # Load the example model
    model = load_test_model(osm_path)

    # Create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    # Get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # Set any custom arguments needed
    # ...

    # Run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # Show the output
    show_output(result)

    # Assert that it ran successfully
    assert_equal('Success', result.value.valueName)

    # Save the modified model for inspection (optional)
    # output_path = File.expand_path('../tests/output/modified_model.osm', __dir__)
    # FileUtils.mkdir_p(File.dirname(output_path))
    # model.save(OpenStudio::Path.new(output_path), true)
  end
end
