class AddTouchesToMultipleChoices < ActiveRecord::Migration[5.1]
  def change
    add_reference :multiple_choices, :touch, foreign_key: true
  end
end
