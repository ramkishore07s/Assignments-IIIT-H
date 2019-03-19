require 'test_helper'

class OperationsControllerTest < ActionDispatch::IntegrationTest
  test "should get editDbs" do
    get operations_editDbs_url
    assert_response :success
  end

  test "should get addTopic" do
    get operations_addTopic_url
    assert_response :success
  end

  test "should get delTopic" do
    get operations_delTopic_url
    assert_response :success
  end

  test "should get addSubTopic" do
    get operations_addSubTopic_url
    assert_response :success
  end

  test "should get delSubTopic" do
    get operations_delSubTopic_url
    assert_response :success
  end

  test "should get addQuestion" do
    get operations_addQuestion_url
    assert_response :success
  end

  test "should get delQuestion" do
    get operations_delQuestion_url
    assert_response :success
  end

end
