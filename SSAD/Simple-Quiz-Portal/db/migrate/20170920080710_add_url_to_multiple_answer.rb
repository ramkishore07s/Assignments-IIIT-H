class AddUrlToMultipleAnswer < ActiveRecord::Migration[5.1]
  def change
    add_column :multiple_answers, :url, :string
  end
end
